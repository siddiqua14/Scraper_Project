import pytest
from scrapy.http import HtmlResponse, Request
from trip_scraper.middlewares import (
    TripScraperSpiderMiddleware,
    TripScraperDownloaderMiddleware,
)

@pytest.fixture
def spider():
    class TestSpider:
        name = "test_spider"
        logger = None

    return TestSpider()


def test_spider_middleware_process_spider_input(spider, caplog):
    middleware = TripScraperSpiderMiddleware()

    # Mock a response
    response = HtmlResponse(url="https://example.com", body=b"Test body")

    # Call process_spider_input
    with caplog.at_level("INFO"):
        result = middleware.process_spider_input(response, spider)

    assert result is None
    assert "Processing response: https://example.com" in caplog.text


def test_downloader_middleware_process_request(spider):
    middleware = TripScraperDownloaderMiddleware()

    # Mock a request with no headers
    request = Request(url="https://example.com", headers={})

    middleware.process_request(request, spider)

    assert request.headers["User-Agent"] == b"TripScraperBot/1.0"


def test_downloader_middleware_preserve_user_agent(spider):
    middleware = TripScraperDownloaderMiddleware()

    # Mock a request with a User-Agent header
    request = Request(url="https://example.com", headers={"User-Agent": "CustomAgent/2.0"})

    middleware.process_request(request, spider)

    assert request.headers["User-Agent"] == b"CustomAgent/2.0"
