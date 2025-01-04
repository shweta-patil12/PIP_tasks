import scrapy
import json

class MyntraSpider(scrapy.Spider):
    name = 'myntra_shoes'
    start_urls = ['https://www.myntra.com/shoes']

    def parse(self, response):
        # Extracting product links and titles from the JSON-LD data
        json_data = response.xpath('//script[contains(text(), "application/ld+json")]/text()').get()
        
        if json_data:
            products = json.loads(json_data)
            for product in products.get('itemListElement', []):
                product_url = product.get('url')
                title = product.get('name')

                yield {
                    'title': title,
                    'url': product_url,
                }

        # Handle pagination (Next Page)
        next_page = response.xpath('//a[contains(@class, "pagination-next")]/@href').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                self.parse,
                meta={'playwright': True}  # Use Playwright to render the page
            )
