import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from trip_scraper.models import Base, Hotel
from trip_scraper.pipelines import DatabasePipeline
from trip_scraper.items import HotelItem

@pytest.fixture(scope="module")
def db_pipeline():
    # Use an in-memory SQLite database for testing
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    pipeline = DatabasePipeline()
    pipeline.session = session
    yield pipeline
    session.close()

def test_process_item(db_pipeline):
    # Test inserting a HotelItem into the database
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
        hotelImg="https://example.com/image.jpg",
        image_path="./images/test.jpg"  # Ensure image_path is set
    )

    processed_item = db_pipeline.process_item(item, None)

    # Verify the item in the database
    hotel = db_pipeline.session.query(Hotel).filter_by(hotel_id=456).one()
    assert hotel.hotelName == "Test Hotel"
    assert hotel.price == 200.0
    assert hotel.city_name == "Test City"
    assert hotel.image_path == "./images/test.jpg"  # Check if image_path is saved correctly
