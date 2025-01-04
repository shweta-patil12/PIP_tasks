import scrapy
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from scrapy.http import HtmlResponse
import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager  # To automatically manage ChromeDriver
from openpyxl import Workbook

class ProductSpider(scrapy.Spider):
    name = 'product_spider'
    allowed_domains = ['amazon.com', 'ebay.com']
    start_urls = []

    def __init__(self):
        # Load input links from input_links.csv
        with open('input_links.csv', mode='r') as file:
            csv_reader = csv.DictReader(file)
            self.start_urls = [row['url'] for row in csv_reader]
        
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Optional: Run Chrome in headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # Initialize the WebDriver with Service and Options
        service = Service(ChromeDriverManager().install())  # Automatically handles ChromeDriver installation
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

        # Set up output Excel file
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(["Name", "Price", "Reviews", "Availability", "URL", "Vendor"])

    def parse(self, response):
        # Handle both static and dynamic pages
        if "amazon.com" in response.url or "ebay.com" in response.url:
            if "amazon.com" in response.url:
                yield from self.parse_amazon(response)
            elif "ebay.com" in response.url:
                yield from self.parse_ebay(response)

            # Pagination logic
            next_page = response.css('li.a-last a::attr(href)').get() or response.css('a.pagination__next::attr(href)').get()
            if next_page:
                yield response.follow(next_page, self.parse)

        elif 'rss' in response.url:
            yield from self.parse_rss(response)

    def parse_amazon(self, response):
        # Parsing Amazon page
        products = response.css('div.s-main-slot div.s-result-item')
        for product in products:
            name = response.xpath('//h2[@class="a-size-medium a-spacing-none a-color-base a-text-normal"]/span/text()').getall()
            price = product.css('span.a-price span.a-offscreen::text').get()
            reviews = product.css('div.a-row span.a-declarative span.a-size-base::text').get()
            availability = product.css('span.a-declarative span.a-size-base::text').get()

            yield {
                'name': name,
                'price': price,
                'reviews': reviews,
                'availability': availability,
                'url': response.url,
                'vendor': 'Amazon'
            }

    def parse_ebay(self, response):
        # Parsing eBay page
        products = response.css('li.s-item')
        for product in products:
            name = product.css('h3.s-item__title::text').get()
            price = product.css('span.s-item__price::text').get()
            reviews = product.css('span.s-item__reviews span::text').get()
            availability = product.css('span.s-item__condition span::text').get()

            yield {
                'name': name,
                'price': price,
                'reviews': reviews,
                'availability': availability,
                'url': response.url,
                'vendor': 'eBay'
            }

    def parse_rss(self, response):
        # Parsing RSS feed
        items = response.xpath('//item')
        for item in items:
            yield {
                'name': item.xpath('title/text()').get(),
                'price': 'N/A',  # You can modify this if price info is available in RSS
                'reviews': 'N/A',
                'availability': 'N/A',
                'url': item.xpath('link/text()').get(),
                'vendor': 'RSS Feed'
            }

    def parse_selenium(self, url):
        # Use Selenium to scrape JavaScript-heavy pages
        self.driver.get(url)
        time.sleep(3)  # Wait for JavaScript to load
        selenium_html = self.driver.page_source
        response = HtmlResponse(url=self.driver.current_url, body=selenium_html, encoding='utf-8')
        self.driver.quit()
        return response

    def closed(self, reason):
        # Save data to Excel when the spider finishes
        self.wb.save("output.xlsx")

