import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from trip_scraper.models import Base, Hotel, db_connect, create_tables

@pytest.fixture(scope="module")
def db_session():
    # Use an in-memory SQLite database for testing
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)  # Create the tables in the in-memory DB
    session = sessionmaker(bind=engine)()
    yield session
    session.close()

def test_table_creation(db_session):
    # Verify that the Hotel table was created
    assert db_session.query(Hotel).count() == 0
    # Add a sample record to ensure the table is functional
    hotel = Hotel(
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
        image_path="/images/test.jpg"
    )
    db_session.add(hotel)
    db_session.commit()

    assert db_session.query(Hotel).count() == 1
    db_session.query(Hotel).filter_by(hotel_id=456).one()
