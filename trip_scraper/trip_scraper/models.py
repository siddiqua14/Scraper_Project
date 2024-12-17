from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()

def db_connect():
    # Read database URL from environment variable or settings
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://scraper_user:scraper_password@db:5432/scraper_db")
    return create_engine(DATABASE_URL)

def create_tables(engine):
    Base.metadata.create_all(engine)

class Hotel(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True, autoincrement=True)
    city_id = Column(Integer, nullable=False)
    city_name = Column(String, nullable=False)
    hotel_id = Column(Integer, unique=True, nullable=False)
    hotelName = Column(String)
    commentScore = Column(Float)
    positionName = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    roomType = Column(String)
    price = Column(Float)
    image_path = Column(String)  # Path to the stored image file