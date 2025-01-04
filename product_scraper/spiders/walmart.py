import scrapy

class WalmartSpider(scrapy.Spider):
    name = "walmart"
    allowed_domains = ["walmart.com"]
    start_urls = [
        "https://www.walmart.com/search/?query=laptops"
    ]
    custom_settings = {
        'DOWNLOADER_CLIENT_TLS_VERIFY': False,
    }

    def parse(self, response):
        # Select all anchor tags with the class 'w-100 h-100 z-1 hide-sibling-opacity  absolute'
        # These are the links that contain the product details
        links = response.css('a.absolute::attr(href)').extract()

        # Print the links to the console (you can also store them in a file or process further)
        for link in links:
            yield {'href': link}

        # You can implement pagination if needed to crawl multiple pages
        next_page = response.css('a.pagination-btn-next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
