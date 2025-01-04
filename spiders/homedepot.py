import scrapy

class HomeDepotSpider(scrapy.Spider):
    name = 'homedepot'
    allowed_domains = ['homedepot.com']
    start_urls = ['https://www.homedepot.com/b/Furniture/N-5yc1vZc7nn']

    def parse(self, response):
        self.logger.info("Parsing HomeDepot page")
        
        # Extracting product titles and links
        titles = response.css('span[data-testid="attribute-product-label"].sui-text-primary.sui-font-regular.sui-text-ellipsis.sui-text-sm.sui-leading-normal.sui-line-clamp-2::text').extract()
        links = response.css('div[data-testid="product-header"] a.sui-font-regular.sui-text-base.sui-tracking-normal.sui-normal-case.sui-line-clamp-unset.sui-font-normal.sui-text-primary.focus-visible\\:sui-bg-focus.focus-visible\\:sui-outline-none.hover\\:sui-underline::attr(href)').extract()

        if not titles or not links:
            self.logger.warning("No product titles or links found on HomeDepot page.")

        # Looping through extracted titles and links and yielding them
        for title, link in zip(titles, links):
            yield {
                'product_name': title.strip(),
                'product_url': response.urljoin(link)
            }
