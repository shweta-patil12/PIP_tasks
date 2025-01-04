import scrapy

class NikeSaleSpider(scrapy.Spider):
    name = 'prices'
    allowed_domains = ['nike.com']
    start_urls = [
        'https://www.nike.com/w/mens-sale-3yaepznik1', 
        'https://www.nike.com/w/clothing-6rive',
        'https://www.nike.com/w/accessories-2vcmn',

    ]

    def parse(self, response):
        # Select product containers on the page
        products = response.css('div.product-card')  # Adjust the product container selector

        for product in products:
            # Extract product link (URL)
            product_link = product.css('a::attr(href)').get()

            # Extract current price (e.g., $81.97)
            current_price = product.css('div.product-price__wrapper div.product-price.is--current-price::text').get()

            # Yield the extracted data
            if product_link and current_price:
                yield {
                    'product_link': product_link,
                    'current_price': current_price.strip(),
                }

        # Pagination handling: Get the URL of the next page (if applicable)
        next_page = response.css('a.pagination-next::attr(href)').get()

        if next_page:
            yield response.follow(next_page, callback=self.parse)
