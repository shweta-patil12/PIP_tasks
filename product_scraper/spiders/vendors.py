import scrapy
import csv
from scrapy.http import HtmlResponse
from selenium import webdriver
from scrapy import Spider
import time
import json
# import response

class ProductSpider(scrapy.Spider):
    name = "vendors"
    
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'DOWNLOADER_IGNORE_SSL_ERRORS': True,
        # 'DOWNLOADER_CLIENTCONTEXTFACTORY': 'scrapy.core.downloader.context.DefaultSslContextFactory',  # Use default context
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            # 'Referer': response.url,
        },
    }


    def start_requests(self):
        with open('input_links.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.logger.info(f"Starting request for URL: {row['url']} with domain: {row['domain']}")
                yield scrapy.Request(url=row['url'], callback=self.parse, meta={'domain': row['domain'].strip().lower()})

    def parse(self, response):
        domain = response.meta['domain']
        self.logger.info(f"Parsing domain: {domain} - URL: {response.url}")
        
        if domain == 'amazon':
            self.logger.info("Calling Amazon parsing")
            return self.parse_amazon(response)
        elif domain == 'ebay':
            self.logger.info("Calling eBay parsing")
            return self.parse_ebay(response)
        elif domain == 'walmart':
            self.logger.info("Calling Walmart parsing")
            return self.parse_walmart(response)
        elif domain == 'flipkart':
            self.logger.info("Calling Flipkart parsing")
            return self.parse_flipkart(response)
        elif domain == 'target':  # Add your target domain name here
            self.logger.info("Calling Target parsing")
            return self.parse_target(response)
        elif domain == 'bestbuy':
            self.logger.info("Calling BestBuy parsing")
            return self.parse_bestbuy(response)
        elif domain == 'nike':
            self.logger.info("Calling Nike parsing")
            return self.parse_nike(response)
        elif domain == 'adidas':
            self.logger.info("Calling Adidas parsing")
            return self.parse_adidas(response)
        elif domain == 'homedepot':
            self.logger.info("Calling Homedepot parsing")
            return self.parse_homedepot(response)
        elif domain == 'myntra':
            self.logger.info("Calling Homedepot parsing")
            return self.parse_myntra(response)
        else:
            self.logger.error(f"Unsupported domain: {domain}")

    def parse_amazon(self, response):
        self.logger.info("Parsing Amazon page")
        product_links = response.css('a.a-link-normal.s-line-clamp-2.s-link-style.a-text-normal::attr(href)').extract()
        product_titles = response.css('a.a-link-normal.s-line-clamp-2.s-link-style.a-text-normal h2 span::text').extract()

        if not product_links or not product_titles:
            self.logger.warning("No product links or titles found on Amazon page.")

        for title, link in zip(product_titles, product_links):
            yield {'product_name': title.strip(), 'product_url': response.urljoin(link)}

    def parse_ebay(self, response):
        self.logger.info("Parsing eBay page")
        
        # Log the first 1000 characters of the eBay page to inspect HTML
        self.logger.info(f"eBay page content: {response.text[:1000]}")

        # Extract product links and titles
        product_links = response.css('a.s-item__link::attr(href)').extract()
        product_titles = response.css('div.s-item__title span::text').extract()

        if not product_links or not product_titles:
            self.logger.warning("No product links or titles found on eBay page.")

        # Yield the product names and URLs
        for title, link in zip(product_titles, product_links):
            yield {'product_name': title.strip(), 'product_url': link}

    def parse_walmart(self, response):
        self.logger.info("Parsing Walmart page")
        
        product_links = response.css('a.absolute::attr(href)').extract()
        product_titles = response.css('span[data-automation-id="product-title"]::text').extract()

        if not product_titles:
            self.logger.warning("No product titles found on Walmart page.")

        for title, link in zip(product_titles, product_links):
            yield {'product_name': title.strip(), 'product_url': response.urljoin(link)}

    def parse_flipkart(self, response):
        self.logger.info("Parsing Flipkart page")

        # XPath for extracting product titles
        # product_titles = response.xpath('//*[@id="container"]/div/div[3]/div[1]/div[2]/div[2]/div/div/div/a/@aria-label').extract()
        product_links = response.css('a.CGtC98::attr(href)').extract()

        # XPath for extracting product links
        # product_titles = response.xpath('//*[@id="container"]/div/div[3]/div[1]/div[2]/div[2]/div/div/div/a/@href').extract()
        product_titles = response.css('div.KzDlHZ::text').extract()


        if not product_titles or not product_links:
            self.logger.warning("No product titles or links found on Flipkart page.")

        for title, link in zip(product_titles, product_links):
            yield {'product_name': title.strip(), 'product_url': response.urljoin(link)}

    def parse_target(self, response):
        self.logger.info("Parsing Target page")
        self.logger.info(f"Response URL: {response.url}")
        self.logger.info(f"Response Headers: {response.headers}")

        # Extract product titles using the aria-label attribute
        product_titles = response.css('div.sc-f8a8939a-0 a[aria-label]::attr(aria-label)').extract()
        # product_titles = response.xpath('//*[@id="pageBodyContainer"]/div/div[1]/div/div/div[4]/div/div/div[6]/div[1]/div/div/div/div[2]/div/div/div[2]/div[1]/div/a/text()').extract()

        # Extract product links using the href attribute
        product_links = response.css('div.sc-f8a8939a-0 a[aria-label]::attr(href)').extract()
        # product_links = response.xpath('//*[@id="pageBodyContainer"]/div/div[1]/div/div/div[4]/div/div/div[6]/div[1]/div/div/div/div[2]/div/div/div[2]/div[1]/div/a/@href').extract()

        if not product_titles or not product_links:
            self.logger.warning("No product titles or links found on Target Domain page.")

        # Yield the product names and URLs
        for title, link in zip(product_titles, product_links):
            yield {'product_name': title.strip(), 'product_url': response.urljoin(link)}

    def parse_bestbuy(self, response):
        self.logger.info("Parsing BestBuy page with Selenium")

        # Set up Selenium WebDriver (Chrome in this case)
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Run in headless mode (no UI)
        driver = webdriver.Chrome(options=options)

        # Use Selenium to open the URL and click the image
        driver.get(response.url)
        
        # Wait for the page to load (you can adjust the sleep time as needed)
        time.sleep(10)  # Wait for 10 seconds (can be adjusted)

        # Click the image (for example, select the 'United States' image based on the src URL)
        img_element = driver.find_element_by_xpath('//img[@src="https://www.bestbuy.com/~assets/bby/_intl/landing_page/images/maps/usa.svg"]')
        img_element.click()

        # Wait for new content to load
        time.sleep(10)  # Wait for 10 seconds after clicking

        # Get the HTML content after JavaScript has been executed
        html = driver.page_source
        driver.quit()

        # Parse the HTML with Scrapy's response
        response = HtmlResponse(url=response.url, body=html, encoding='utf-8')

        # Continue extracting product data as you did before
        product_links = response.css('a[href*="skuId"]::attr(href)').extract()
        product_titles = response.css('a[href*="skuId"]::text').extract()

        for title, link in zip(product_titles, product_links):
            yield {'product_name': title.strip(), 'product_url': response.urljoin(link)}


    # New method for Nike
    def parse_nike(self, response):
        self.logger.info("Parsing nike page")
        product_links = response.css('a.product-card__link-overlay::attr(href)').extract()
        product_titles = response.css('div.product-card__title::text').extract()
        product_subtitles = response.css('div.product-card__subtitle::text').extract()


        if not product_titles or not product_links:
            self.logger.warning("No product titles or links found on Nike page.")

        for title, link, subtitle in zip(product_titles, product_links, product_subtitles):
            combined_title = f"{title.strip()} - {subtitle.strip()}"
            yield {'product_name': combined_title, 'product_url': link}

    def parse_adidas(self, response):
        self.logger.info("Parsing Adidas page")
        
        # Extract product link and title for Adidas domain
        product_links = response.css('a[data-testid="product-card-description-link"]::attr(href)').extract()
        product_titles = response.css('p.product-card-description_name__xHvJ2::text').extract()
        product_subtitles = response.css('p.product-card-description_info__z_CcT::text').extract()

        if not product_links or not product_titles:
            self.logger.warning("No product links or titles found on Adidas page.")

        for title, link, subtitle in zip(product_titles, product_links):
            combined_title = f"{title.strip()} - {subtitle.strip()}" if subtitle else title.strip()
            yield {'product_name': combined_title, 'product_url': response.urljoin(link)}

    def parse_homedepot(self, response):
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

    def parse_myntra(self, response):
        # Find the <script> tag containing the JSON-LD data
        script_data = response.css('script[type="application/ld+json"]::text').get()

        # If JSON-LD script is found, parse the JSON
        if script_data:
            # Parse the JSON
            data = json.loads(script_data)

            # Extract product titles and URLs
            for item in data.get("itemListElement", []):
                title = item.get("name")
                url = item.get("url")

                # Yield the extracted product data
                if title and url:
                    yield {
                        'product_name': title.strip(),
                        'product_url': url.strip()
                    }

        else:
            self.logger.warning("No JSON-LD data found on Myntra page.")
