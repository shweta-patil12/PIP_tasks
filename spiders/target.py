from scrapy_selenium import SeleniumRequest
import time
import scrapy

class TargetSpider(scrapy.Spider):
    name = 'target'
    
    def start_requests(self):
        yield SeleniumRequest(
            url="https://www.target.com/s?searchTerm=laptops",
            callback=self.parse,
            wait_time=5  # Add some wait time to ensure page is fully rendered
        )

    def parse(self, response):
        self.logger.info("Parsing Target page")
        self.logger.info(f"Response URL: {response.url}")
        self.logger.info(f"Response Headers: {response.headers}")

        # Extract product titles from the <div> with the class 'styles_truncate__Eorq7'
        product_titles = response.css('a[data-test="product-title"] div.styles_truncate__Eorq7::text').getall()

        # Extract product links from the <a> tag's href attribute
        product_links = response.css('a[data-test="product-title"]::attr(href)').getall()

        if not product_titles or not product_links:
            self.logger.warning("No product titles or links found on Target Domain page.")

        # Yield the product names and URLs
        for title, link in zip(product_titles, product_links):
            yield {'product_name': title.strip(), 'product_url': response.urljoin(link)}
