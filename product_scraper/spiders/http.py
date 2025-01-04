import scrapy
import pandas as pd
import numpy as np
from scrapy.http import HtmlResponse

class HomeDepotSpider(scrapy.Spider):
    name = "new"
    allowed_domains = ["homedepot.com"]
    
    start_urls = [
        "https://www.homedepot.com/b/Furniture/N-5yc1vZc7nn"
    ]

    def parse(self, response):
        # Extract product links from the main page
        links = response.css('div[data-testid="product-header"] a.sui-font-regular.sui-text-base.sui-tracking-normal.sui-normal-case.sui-line-clamp-unset.sui-font-normal.sui-text-primary.focus-visible\\:sui-bg-focus.focus-visible\\:sui-outline-none.hover\\:sui-underline::attr(href)').getall()

        for link in links:
            # Follow the link to the product page
            yield response.follow(link, callback=self.parse_product)
        
        # Pagination - if there's a next page, follow it
        next_page = response.css('a.pagination__next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_product(self, response):
        # Extract title
        title = self.get_title(response)
        
        # Extract price
        price = self.get_price(response)
        
        # Extract rating
        rating = self.get_rating(response)
        
        # Extract review count
        review_count = self.get_review_count(response)
        
        # Extract availability
        availability = self.get_availability(response)

        # Yield the scraped data as a dictionary
        yield {
            'title': title,
            'price': price,
            'rating': rating,
            'reviews': review_count,
            'availability': availability,
            'product_url': response.url
        }

    def get_title(self, response):
        try:
            title = response.css('span[data-component="product-details:ProductDetailsTitle:v9.13.1"] h1.sui-h4-bold::text').get().strip()
        except AttributeError:
            title = ""
        return title

    def get_price(self, response):
        try:
            # Extract price components
            dollar_sign = response.css('div.sui-flex.sui-flex-row.sui-leading-none span.sui-font-display.sui-text-3xl::text').get().strip()
            integer_part = response.css('div.sui-flex.sui-flex-row.sui-leading-none span.sui-font-display.sui-text-9xl::text').get().strip()
            decimal_part = response.css('div.sui-flex.sui-flex-row.sui-leading-none span.sui-sr-only::text').get().strip()
            
            # Combine parts to form the full price
            price = f"{dollar_sign}{integer_part}{decimal_part}"
        except AttributeError:
            price = ""
        return price
    
    def get_rating(self, response):
        try:
            rating_text = response.css('div.sui-flex.sui-mt-1.sui-items-center.sui-h-5 p.sui-font-regular.sui-text-base.sui-tracking-normal.sui-normal-case.sui-line-clamp-unset.sui-font-normal.sui-text-subtle::text').get().strip()
            # Extract the numeric rating from the text (e.g., "4.7 out of 5")
            rating = rating_text.split(' out ')[0]
        except AttributeError:
            rating = ""
        return rating

    def get_review_count(self, response):
        try:
            review_count_text = response.css('div.sui-flex.sui-mt-1.sui-items-center.sui-h-5 span.sui-font-regular.sui-text-xs.sui-leading-tight.sui-tracking-normal.sui-normal-case.sui-line-clamp-unset.sui-font-normal.sui-text-primary::text').get().strip()
            # Extract the number from the review count text (e.g., "3,259")
            review_count = review_count_text.strip('()')
        except AttributeError:
            review_count = ""
        return review_count

    def get_availability(self, response):
        try:
            # Capture all text within the availability section
            availability_text = response.css('span.sui-ml-1::text').get().strip()
        except AttributeError:
            availability_text = "Availability information not found."
        return availability_text


    # def close(self, reason):
    #     # After the spider closes, save the data to CSV
    #     df = pd.DataFrame(self.crawler.stats.get_value('item_scraped_count'))
    #     df['title'].replace('', np.nan, inplace=True)
    #     df.dropna(subset=['title'], inplace=True)
    #     df.to_csv("homedepot_data.csv", header=True, index=False)
