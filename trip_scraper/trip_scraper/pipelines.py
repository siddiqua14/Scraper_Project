import os
import requests
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from .models import Hotel, Base, create_tables, db_connect

class DatabasePipeline:
    def __init__(self):
        # Database connection setup
        self.engine = db_connect()  # Use db_connect for engine
        create_tables(self.engine)  # Create tables if they don't exist
        self.Session = sessionmaker(bind=self.engine)
        self.session = None

        # Ensure images directory exists
        if not os.path.exists('./images'):
            os.makedirs('./images')

    def open_spider(self, spider):
        # Create a session when the spider starts
        self.session = self.Session()

    def close_spider(self, spider):
        # Commit the transaction and close the session when the spider ends
        if self.session:
            self.session.commit()
            self.session.close()

    def process_item(self, item, spider):
        # Check and unwrap lists before inserting into database
        for key, value in item.items():
            if isinstance(value, list) and value:  # If value is a list and not empty
                item[key] = value[0]  # Take the first element of the list
            elif isinstance(value, list):  # Handle empty lists
                item[key] = None

        # Download the image
        image_url = item.get("hotelImg")
        if image_url:
            image_name = f"{item['hotel_id']}.jpg"
            image_path = os.path.join('./images', image_name)
            response = requests.get(image_url)

            if response.status_code == 200:
                with open(image_path, 'wb') as file:
                    file.write(response.content)
                item["image_path"] = f"./images/{image_name}"

        # Insert the data into the database
        hotel = Hotel(
            city_id=item['city_id'],
            city_name=item['city_name'],
            hotel_id=item['hotel_id'],
            hotelName=item['hotelName'],
            commentScore=item['commentScore'],
            positionName=item['positionName'],
            latitude=item['latitude'],
            longitude=item['longitude'],
            roomType=item['roomType'],
            price=item['price'],
            image_path=item['image_path']
        )

        self.session.add(hotel)
        self.session.commit()
        return item