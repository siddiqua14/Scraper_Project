# Scrapy settings for trip_scraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "trip_scraper"

SPIDER_MODULES = ["trip_scraper.spiders"]
NEWSPIDER_MODULE = "trip_scraper.spiders"


# Enable logging for debugging
#LOG_LEVEL = 'DEBUG'
# Logging
LOG_LEVEL = 'INFO'
# Delay between requests
DOWNLOAD_DELAY = 5  # 3 seconds (adjust as needed)

# Enable randomization of delay
RANDOMIZE_DOWNLOAD_DELAY = True

# Concurrent requests settings
CONCURRENT_REQUESTS = 1  # Optional: Reduce concurrency for gentler scraping
# Crawl responsibly by identifying yourself (and your website) on the user-agent
# Custom User-Agent
USER_AGENT = 'trip_hotel_scraper (https://yourwebsite.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Set settings whose default value is deprecated to a future-proof value
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"



# Configure the item pipeline
ITEM_PIPELINES = {
    'trip_scraper.pipelines.DatabasePipeline': 1,
}

IMAGES_STORE = './images'

# Database URL (read from Docker environment)
DATABASE_URL = "psql postgresql://scraper_user:scraper_password@db:5432/scraper_db"
# Add the necessary settings for database connection
SQLALCHEMY_DATABASE_URI = DATABASE_URL
SQLALCHEMY_TRACK_MODIFICATIONS = False
