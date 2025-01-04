import scrapy
import csv

class ProductNameSpider(scrapy.Spider):
    name = 'names'
    
    # Start with an empty list of URLs
    start_urls = []
    
    def __init__(self, *args, **kwargs):
        super(ProductNameSpider, self).__init__(*args, **kwargs)
        
        # Read the product URLs from the links.csv file
        with open('links.csv', mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header
            self.start_urls = [row[0] for row in reader if row]  # Extract URLs from the first column
    
    def parse(self, response):
        # Extract product name from h1 tag (customize as needed based on each site)
        # product_name = response.css('h1::text').get().strip() if response.css('h1::text').get() else 'No product name found'
        product_name_parts = response.css('h1 *::text').getall()

        # Join the extracted text parts and clean up (remove extra spaces, newlines, etc.)
        product_name = ' '.join([part.strip() for part in product_name_parts if part.strip()])

        # If no product name is found, provide a default message
        if not product_name:
            product_name = 'No product name found'

        # Save the product name and original URL to CSV
        with open('name.csv', mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([product_name, response.url])
        
        # Log to indicate that the product information has been scraped
        self.log(f'Scraped: {product_name} from {response.url}')

