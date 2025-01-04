import scrapy
import csv

class ProductSpider(scrapy.Spider):
    name = "new_spider"
    
    def start_requests(self):
        with open('input_links.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.logger.info(f"Starting request for URL: {row['url']} with domain: {row['domain']}")
                yield scrapy.Request(url=row['url'], callback=self.parse, meta={'domain': row['domain']})

    def parse(self, response):
        domain = response.meta['domain']
        self.logger.info(f"Parsing domain: {domain} - URL: {response.url}")
        
        if domain == 'amazon':
            return self.parse_amazon(response)
        elif domain == 'ebay':
            return self.parse_ebay(response)
        elif domain == 'walmart':
            return self.parse_walmart(response)
        else:
            self.logger.error(f"Unsupported domain: {domain}")

    def parse_amazon(self, response):
        self.logger.info("Parsing Amazon page")
        product_links = response.css('a.a-link-normal.a-text-normal::attr(href)').extract()
        product_links = [response.urljoin(link) for link in product_links]
        
        for link in product_links:
            yield {'product_url': link}

        next_page = response.css('li.a-last a::attr(href)').extract_first()
        if next_page:
            yield response.follow(next_page, self.parse_amazon)

    def parse_ebay(self, response):
        self.logger.info("Parsing eBay page")
        product_links = response.css('a.s-item__link::attr(href)').extract()
        for link in product_links:
            yield {'product_url': link}
        
        next_page = response.css('a.pagination__next::attr(href)').extract_first()
        if next_page:
            yield response.follow(next_page, self.parse_ebay)

    def parse_walmart(self, response):
        self.logger.info("Parsing Walmart page")
        product_links = response.xpath('//a[contains(@class, "product-title")]/@href').extract()
        for link in product_links:
            yield {'product_url': response.urljoin(link)}
        
        next_page = response.css('a.pagination-btn-next::attr(href)').extract_first()
        if next_page:
            yield response.follow(next_page, self.parse_walmart)