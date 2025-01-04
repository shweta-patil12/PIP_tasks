import scrapy
import pandas as pd
import numpy as np
from scrapy.http import HtmlResponse

class AmazonSpider(scrapy.Spider):
    name = "amazon"
    allowed_domains = ["amazon.com"]
    
    start_urls = [
        "https://www.amazon.com/s?k=playstation+4&ref=nb_sb_noss_2"
    ]

    def parse(self, response):
        # Extract product links from the main page
        links = response.css('a.a-link-normal.s-no-outline::attr(href)').getall()

        for link in links:
            # Follow the link to the product page
            yield response.follow(link, callback=self.parse_product)
        
        # Pagination - if there's a next page, follow it
        next_page = response.css('ul.a-pagination li.a-last a::attr(href)').get()
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
            'availability': availability
        }

    def get_title(self, response):
        try:
            title = response.css('span#productTitle::text').get().strip()
        except AttributeError:
            title = ""
        return title

    def get_price(self, response):
        try:
            price = response.css('span#priceblock_ourprice::text').get().strip()
        except AttributeError:
            try:
                price = response.css('span#priceblock_dealprice::text').get().strip()
            except AttributeError:
                price = ""
        return price

    def get_rating(self, response):
        try:
            rating = response.css('i.a-icon.a-icon-star.a-star-4-5::text').get().strip()
        except AttributeError:
            try:
                rating = response.css('span.a-icon-alt::text').get().strip()
            except AttributeError:
                rating = ""
        return rating

    def get_review_count(self, response):
        try:
            review_count = response.css('span#acrCustomerReviewText::text').get().strip()
        except AttributeError:
            review_count = ""
        return review_count

    def get_availability(self, response):
        try:
            availability = response.css('div#availability span.a-declarative span.a-size-medium::text').get().strip()
        except AttributeError:
            availability = "Not Available"
        return availability

    def close(self, reason):
        # After the spider closes, save the data to CSV
        df = pd.DataFrame(self.crawler.stats.get_value('item_scraped_count'))
        df['title'].replace('', np.nan, inplace=True)
        df.dropna(subset=['title'], inplace=True)
        df.to_csv("amazon_data.csv", header=True, index=False)

