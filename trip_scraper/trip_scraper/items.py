import scrapy

class HotelItem(scrapy.Item):
    city_id = scrapy.Field()
    city_name = scrapy.Field()
    hotel_id = scrapy.Field()
    hotelName = scrapy.Field()
    commentScore = scrapy.Field()
    positionName = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    roomType = scrapy.Field()
    price = scrapy.Field()
    hotelImg = scrapy.Field()
    image_path = scrapy.Field()
