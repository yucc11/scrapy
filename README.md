# Carrefour and Watsons Scraper

This repository is a Scrapy-based web crawler for extracting product data from [Carrefour](https://online.carrefour.com.tw/) and [Watsons](https://www.watsons.com.tw/) websites. The scraper collects product details, prices, images, and other relevant information.

## How to use

1. Clone the repository:
    ```sh
    git clone $REMOTE_URL$
    ```
2. Navigate to the project directory:
    ```sh
    cd $REPO_NAME$
    ```
3. Run the Scrapy spider for Carrefour:
    ```sh
    scrapy crawl carrefour
    ```
3. Run the Scrapy spider for Watsons:
    ```sh
    scrapy crawl watsons
    ```
4. The scraped data will be stored in `MongoDB`.

