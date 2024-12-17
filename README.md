# Trip Scraper Project

This project is a web scraping application built using Scrapy that scrapes hotel information from Trip.com. The scraped data is stored in a PostgreSQL database. The project is containerized using Docker for easy deployment and development.


## Table of Contents

- [Prerequisites](#prerequisites)
- [How to Run the Project](#how-to-run-the-project)
  - [1. Set Up Docker](#1-set-up-docker)
  - [2. Build and Run Containers](#2-build-and-run-containers)
  - [3. Scraping Process](#3-scraping-process)
  - [4. Accessing the Data](#4-accessing-the-data)
  - [5. Storing Images](#5-storing-images)
- [Configuration](#configuration)
  - [Settings File](#settings-file)
  - [Database Configuration](#database-configuration)
  - [Scrapy Pipeline](#scrapy-pipeline)
  - [Models](#models)
- [Test and Coverage Results](#test-and-coverage-results)
- [Troubleshooting](#troubleshooting)


## Prerequisites

Before getting started, ensure you have the following installed on your machine:

- **Docker**: For running the application in containers.
- **Docker Compose**: For managing multi-container Docker applications.
- **Python 3.12 or later**: Required for running Scrapy and other dependencies.
- **PostgreSQL**: A PostgreSQL database to store the scraped data.


## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/siddiqua14/Scraper_Project.git
   cd Scraper_Project
   ```
2. Set up a virtual environment (optional but recommended):

    ```bash 
    python3 -m venv .venv       # python -m venv .venv
    source .venv/bin/activate   # On Windows, use .venv\Scripts\activate
    ```

3. Go to the `trip_scraper` for scraper run
    ```bash
    cd trip_scraper
    ```

3. Install required Python dependencies:

    ```bash
    pip install -r requirements.txt
    ```
    - `Scrapy`: The main library for scraping.
    - `SQLAlchemy`: Used for interacting with the PostgreSQL database.
    - `requests`: For downloading images.

4. **Docker**
The project is containerized with Docker to simplify setup. Docker Compose is used to set up both the Scrapy spider and the PostgreSQL database in separate containers.
## How to Run the Project
Follow these steps to run the project locally or in a containerized environment:
1. **Set Up Docker:**
    Ensure Docker and Docker Compose are installed. If not, follow the installation guide:
    - Install Docker
    - Install Docker Compose

2. **Build and Run Containers:**
    Once Docker is installed, run the following command to build and start the containers:
    ```bash
    docker-compose up --build
    ```
    This will:
    - Build the Docker images defined in Dockerfile.
    - Start a PostgreSQL container for storing the scraped data.
    - Start the Scrapy spider to scrape hotel data from Trip.com.

3. **Scraping Process**
The spider starts by scraping hotel information from Trip.com. It:

- Scrapes data from a list of cities.
- Chooses a random city to extract hotel data.
- Extracts hotel details like name, price, location, and reviews.
- Downloads hotel images and stores them locally in the images/ directory.
- Stores the scraped data in the PostgreSQL database defined in the settings.
4. **Accessing the Data** 
The scraped hotel data is saved in the PostgreSQL database. To access the database, use the following connection command:
    ```bash
    docker exec -it postgres_db psql -U scraper_user -d scraper_db
    ```
    This command opens a PostgreSQL interactive terminal inside your postgres_db container, where:
    - `-it` allows interactive terminal access.
    - `psql` is the PostgreSQL command-line client.
    - `-U` scraper_user specifies the user (scraper_user).
    - -`d` scraper_db specifies the database (scraper_db).

    Check the Data in the Table:
    Once you're inside the PostgreSQL terminal, you can query the hotels table to check the data:
    ```bash
    SELECT * FROM hotels;
    ```
    This command will return all the rows stored in the hotels table, including the fields like city_id, city_name, hotel_id, hotelName, commentScore, and others that your spider scraped.
5. **Storing Images**
Hotel images are downloaded and saved to the images/ directory. The image URL is also stored in the database to reference the downloaded image.

## Configuration
1. **Settings File**
The settings.py file contains configuration for the Scrapy spider. Some important settings include:
- LOG_LEVEL: Set to INFO to provide detailed logs during scraping.
- DOWNLOAD_DELAY: Delay between requests to avoid overloading the server.
- USER_AGENT: Custom user agent to identify the scraper.
- ITEM_PIPELINES: Pipeline for saving data to the PostgreSQL database.
2. **Database Configuration**
    The database URL is configured in the settings.py and models.py files:
``` DATABASE_URL = "postgresql://scraper_user:scraper_password@db:5432/scraper_db" ```
Change the URL if needed, especially if you're running the database outside of Docker.

3. **Scrapy Pipeline**
The DatabasePipeline in pipelines.py handles saving the scraped data into the PostgreSQL database. It also downloads hotel images and stores them locally.

4. **Models**
The Hotel class in models.py defines the database structure using SQLAlchemy ORM. It maps the scraped hotel data to the hotels table in PostgreSQL.


## Test and Coverage Results
Before running the tests, ensure the following dependencies are installed:

- **pytest**: Testing framework
- **coverage**: Code coverage tool
- **Scrapy**: Web scraping framework
- **unittest.mock**: Mocking library for unit tests

After the container finishes running the spider:
- Access the container's shell:
```bash
docker exec -it scrapy_app bash
```
- Generate the coverage report:
```bash
pytest --cov=trip_scraper --cov-report=term-missing
```
This will generate a code coverage report for your Scrapy spider.

## Troubleshooting
- If you encounter issues with database connections, ensure that the PostgreSQL container is running and accessible.
- For issues with scraping, check the Scrapy logs for errors and ensure that the website structure hasn't changed.
- ### Database Issues
    If you encounter issues with storing data in the database, it might be helpful to drop and recreate the `hotels` table. This can be done without dropping the entire database.
    #### Steps to Drop and Rebuild the `hotels` Table:

    1. **Connect to PostgreSQL**: Access the PostgreSQL container using the following command:

        ```bash
        docker exec -it postgres_db psql -U scraper_user -d scraper_db
        ```

        Replace `postgres_db` with the name of your PostgreSQL container if it's different.

    2. **Connect to the Database**: Connect to the `scraper_db` (or your relevant database):

        ```sql
        \c scraper_db;
        ```

    3. **Drop the `hotels` Table**: Drop the `hotels` table using the following command:

        ```sql
        DROP TABLE hotels;
        ```

    4. **Rebuild the Table**: You can now rebuild the `hotels` table by running your Scrapy spider, which will automatically create the table if it doesn't exist and populate it with new data.

        Alternatively, if you have a script for creating tables, you can manually execute it to recreate the schema.

    5. **Exit PostgreSQL**: Once done, exit the PostgreSQL prompt by typing:

        ```sql
        \q
        ```

    By following these steps, you can ensure that the `hotels` table is reset and data is inserted again.