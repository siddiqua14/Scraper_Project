import pytest
from scrapy.http import HtmlResponse
from unittest.mock import patch
from trip_scraper.spiders.hotel import HotelsSpider


@pytest.fixture
def spider():
    return HotelsSpider()


# Test parse method when 'inboundCities' contains cities
def test_parse_city_inbound(spider):
    body = """
    <script>
    window.IBU_HOTEL = {
        "initData": {
            "htlsData": {
                "inboundCities": [{"id": "1", "name": "Test City"}],
                "outboundCities": []
            }
        }
    };
    </script>
    """
    response = HtmlResponse(url="https://example.com", body=body, encoding="utf-8")
    results = list(spider.parse(response))

    # Assert that a single result is returned and contains the expected URL
    assert len(results) == 1
    assert "trip.com" in results[0].url


# Test parse method when 'outboundCities' contains cities
def test_parse_city_outbound(spider):
    body = """
    <script>
    window.IBU_HOTEL = {
        "initData": {
            "htlsData": {
                "inboundCities": [],
                "outboundCities": [{"id": "2", "name": "Another City"}]
            }
        }
    };
    </script>
    """
    response = HtmlResponse(url="https://example.com", body=body, encoding="utf-8")
    results = list(spider.parse(response))

    # Assert that a single result is returned and contains the expected URL
    assert len(results) == 1
    assert "trip.com" in results[0].url


# Test parse_hotel_list when hotel data is present
def test_parse_hotel_list(spider):
    body = """
    <script>
    window.IBU_HOTEL = {
        "initData": {
            "firstPageList": {
                "hotelList": [{
                    "hotelBasicInfo": {"hotelId": 456, "hotelName": "Test Hotel", "price": 150.0},
                    "commentInfo": {"commentScore": 4.5},
                    "positionInfo": {"positionName": "Downtown", "coordinate": {"lat": 12.34, "lng": 56.78}},
                    "roomInfo": {"physicalRoomName": "Suite"}
                }]
            }
        }
    };
    </script>
    """
    response = HtmlResponse(url="https://example.com/hotels", body=body, encoding="utf-8")
    results = list(spider.parse_hotel_list(response))

    assert len(results) == 1
    hotel = results[0]
    assert hotel["hotel_id"] == 456
    assert hotel["hotelName"] == "Test Hotel"
    assert hotel["price"] == 150.0
    assert hotel["commentScore"] == 4.5
    assert hotel["positionName"] == "Downtown"
    assert hotel["latitude"] == 12.34
    assert hotel["longitude"] == 56.78


# Test parse_hotel_list when hotel list is empty
def test_parse_hotel_list_empty(spider):
    body = """
    <script>
    window.IBU_HOTEL = {
        "initData": {
            "firstPageList": {
                "hotelList": []
            }
        }
    };
    </script>
    """
    response = HtmlResponse(url="https://example.com/empty-hotels", body=body, encoding="utf-8")
    results = list(spider.parse_hotel_list(response))

    # Assert no hotels are returned
    assert len(results) == 0


# Test parse_hotel_list when fields are missing
def test_parse_hotel_list_missing_fields(spider):
    body = """
    <script>
    window.IBU_HOTEL = {
        "initData": {
            "firstPageList": {
                "hotelList": [{
                    "hotelBasicInfo": {
                        "hotelId": 123
                    },
                    "commentInfo": {},
                    "positionInfo": {},
                    "roomInfo": {}
                }]
            }
        }
    };
    </script>
    """
    response = HtmlResponse(url="https://example.com/missing-fields", body=body, encoding="utf-8")
    results = list(spider.parse_hotel_list(response))

    # Assert one result is returned with missing fields defaulted to None
    assert len(results) == 1
    hotel = results[0]
    assert hotel["hotel_id"] == 123
    assert hotel.get("hotelName") is None
    assert hotel.get("price") is None
    assert hotel.get("commentScore") is None
    assert hotel.get("positionName") is None
    assert hotel.get("latitude") is None
    assert hotel.get("longitude") is None


# Test error handling when no script is found in the page
@patch("trip_scraper.spiders.hotel.HotelsSpider.logger.error")
def test_parse_no_script_found(mock_error, spider):
    body = "<html><head></head><body>No hotel data here.</body></html>"
    response = HtmlResponse(url="https://example.com/no-script", body=body, encoding="utf-8")
    result = list(spider.parse(response))

    # Assert that the error method was called
    mock_error.assert_called_with("No script containing 'window.IBU_HOTEL' found!")
    assert len(result) == 0


# Test error handling when JSON cannot be decoded
@patch("trip_scraper.spiders.hotel.HotelsSpider.logger.error")
def test_parse_json_decode_error(mock_error, spider):
    body = """
    <script>
    window.IBU_HOTEL = {
        "initData": {
            "htlsData": {
                "inboundCities": [{"id": "1", "name": "Test City"}]
            }
        }
    };
    </script>
    """
    # Simulate a malformed JSON (missing closing bracket)
    malformed_body = body.replace("};", "")
    response = HtmlResponse(url="https://example.com/malformed-json", body=malformed_body, encoding="utf-8")
    result = list(spider.parse(response))

    # Assert that the error method was called for JSONDecodeError
    mock_error.assert_called_with("Failed to decode JSON:")
    assert len(result) == 0
