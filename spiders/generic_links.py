import scrapy
import csv
import re

class GenericProductLinkSpider(scrapy.Spider):
    name = 'generic'

    # List of start URLs from different websites
    start_urls = [
        'https://www.walmart.com/search/?query=smartphones',
        'https://www.nike.com/w/shoes-3yaepznik1',
        "https://www.target.com/s?searchTerm=laptops",
    ]
    
    def __init__(self, *args, **kwargs):
        super(GenericProductLinkSpider, self).__init__(*args, **kwargs)
        self.seen_urls = set()  # Set to store unique URLs
    
    def parse(self, response):
        # Extract all anchor tags (<a>) with potential product links
        links = response.css('a::attr(href)').getall()

        # Filter links based on generic product URL patterns
        for link in links:
            # Skip empty or None links
            if not link:
                continue

            # Normalize relative URLs to absolute URLs
            link = response.urljoin(link)

            # Define patterns for product links (commonly contain keywords like 'dp', 'product', 'item')
            product_patterns = [
                r'/dp/',               # Amazon product pages
                r'/product/',          # General product page indicator
                r'/item/',             # eBay product item pages
                r'/p/',                # Target product pages
                r'/ip/',               # Walmart product pages
                r'/catalog/product/',  # Myntra, Adidas, Nike product pages
                r'/shop/',             # Product pages on Walmart
                r'/products/',         # Generic term for product pages
                r'/en-us/product/',    # Common pattern on many eCommerce sites
                r'/shop/p/',           # Newegg product pages
            ]
            
            # Check if the link matches any of the product patterns
            if any(re.search(pattern, link) for pattern in product_patterns):
                # Add only unique URLs to the set
                self.seen_urls.add(link)

        # Log the number of unique URLs found so far
        self.log(f'Found {len(self.seen_urls)} unique product links so far')

        # Pagination: Find and follow the "next" page link if it exists
        next_page = self.get_next_page(response)
        if next_page:
            yield response.follow(next_page, self.parse)

    def get_next_page(self, response):
        """
        Helper method to extract and return the "next" page URL if available.
        This method attempts common pagination selectors for various websites.
        """
        next_page = None

        # Common selectors for pagination that work for most eCommerce sites
        next_page_selectors = [
            'a.s-pagination-next::attr(href)',      # Amazon, Walmart, Flipkart
            'a.pagination__next::attr(href)',       # eBay, BestBuy, Target
            'a.pagination-next::attr(href)',        # BestBuy
            'a.page-next::attr(href)',              # Home Depot, Newegg
            'a.next-pagination::attr(href)',        # Nike, Myntra
            'a._1LKpS3::attr(href)',               # Flipkart specific
            'a.next::attr(href)',                  # Target, Walmart
        ]

        # Try all pagination selectors
        for selector in next_page_selectors:
            next_page = response.css(selector).get()
            if next_page:
                break

        # If a next page URL is found, return it
        return next_page

    def closed(self, reason):
        # Save unique URLs to CSV when the spider finishes
        with open('links.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Product URL'])  # Write header
            for url in self.seen_urls:
                writer.writerow([url])
        
        # Log when the spider has finished saving URLs
        self.log(f'Saved {len(self.seen_urls)} unique product links to links.csv')
