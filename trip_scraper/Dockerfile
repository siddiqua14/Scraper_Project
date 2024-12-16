# Dockerfile for Scrapy Project
FROM python:3.12-slim
ENV PYTHONPATH=/app

WORKDIR /app

RUN apt-get update && apt-get install -y gcc libpq-dev

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# CMD ["scrapy", "crawl", "random"]
CMD ["sh", "-c", "scrapy crawl hotel && tail -f /dev/null"]
# Set the default command to use coverage
# CMD ["sh", "-c", "coverage run -m scrapy crawl hotel && tail -f /dev/null"]
