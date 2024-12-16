from trip_scraper.items import HotelItem

def test_hotel_item():
    # Verify HotelItem with sample data
    item = HotelItem(
        city_id=123,
        city_name="Test City",
        hotel_id=456,
        hotelName="Test Hotel",
        commentScore=4.5,
        positionName="Downtown",
        latitude=12.34,
        longitude=56.78,
        roomType="Suite",
        price=200.0,
        hotelImg="https://example.com/image.jpg"
    )

    assert item["city_id"] == 123
    assert item["hotelName"] == "Test Hotel"
    assert item["price"] == 200.0
    assert item["hotelImg"] == "https://example.com/image.jpg"
