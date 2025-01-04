import scrapy
import pandas as pd
import numpy as np

class AdidasSpider(scrapy.Spider):
    name = "adidas"
    allowed_domains = ["adidas.com"]
    
    start_urls = [
        "https://www.adidas.com/us/men-shoes"
    ]

    def parse(self, response):
        # Extract product links from the main page
        product_links = response.css('a[data-testid="product-card-description-link"]::attr(href)').getall()

        for link in product_links:
            # Follow the link to the product page
            yield response.follow(link, callback=self.parse_product)
        
        # Pagination - if there's a next page, follow it
        next_page = response.css('a.pagination__next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_product(self, response):
        # Extract product name, link, and price
        title = self.get_title(response)
        price = self.get_price(response)
        
        # Yield the scraped data as a dictionary
        yield {
            'product_name': title,
            'product_url': response.url,
            'product_price': price,
        }

    def get_title(self, response):
        try:
            title = response.css('p.product-card-description_name__xHvJ2::text').get().strip()
        except AttributeError:
            title = ""
        return title

    def get_price(self, response):
        try:
            price = response.css('div.gl-price-item::text').get().strip()
        except AttributeError:
            price = ""
        return price

    def close(self, reason):
        # Ensure items were scraped before attempting to save them to CSV
        if self.crawler.stats.get_value('item_scraped_count') > 0:
            # Only proceed if there are scraped items
            output_data = []
            for item in self.crawler.stats.get_value('item_scraped_count'):
                output_data.append(item)

            # Create a DataFrame with the scraped data and save to CSV
            df = pd.DataFrame(output_data)
            df['product_name'].replace('', np.nan, inplace=True)
            df.dropna(subset=['product_name'], inplace=True)
            df.to_csv("adidas_data.csv", header=True, index=False)
        else:
            self.logger.info("No items were scraped, skipping CSV export.")
