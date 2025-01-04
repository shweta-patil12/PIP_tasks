import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BestBuyLaptopSpider(scrapy.Spider):
    name = "bestbuy"
    
    # Starting URL
    start_urls = [
        "https://www.bestbuy.com/site/searchpage.jsp?st=laptops"
    ]
    
    def start_requests(self):
        for url in self.start_urls:
            # Use SeleniumRequest to open the URL and pass control to the parse method
            yield SeleniumRequest(url=url, callback=self.parse)

    def parse(self, response):
        driver = response.meta['driver']


        # Extract product details like name, price, etc.
        products = driver.find_elements_by_css_selector('.sku-item')

        for product in products:
            title = product.find_element_by_css_selector('.sku-header a').text
            price = product.find_element_by_css_selector('.priceView-hero-price span').text
            product_url = product.find_element_by_css_selector('.sku-header a').get_attribute('href')
            
            yield {
                'title': title,
                'price': price,
                'url': product_url
            }
        
        # Pagination - Check if there's a next page and follow it
        try:
            next_page = driver.find_element_by_css_selector('.pagination-next a')
            if next_page:
                yield SeleniumRequest(url=next_page.get_attribute('href'), callback=self.parse)
        except Exception as e:
            self.logger.info(f"No next page found: {e}")
