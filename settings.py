# Scrapy settings for the product_scraper project

# For detailed settings, refer to the Scrapy documentation:
# https://docs.scrapy.org/en/latest/topics/settings.html
# https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'product_scraper'

# Spider modules and new spider module for generating new spiders
SPIDER_MODULES = ['product_scraper.spiders']
NEWSPIDER_MODULE = 'product_scraper.spiders'

# Download settings
DOWNLOAD_TIMEOUT = 200  # Timeout duration for downloads (in seconds)
RETRY_TIMES = 3  # Number of retry attempts on failure
DOWNLOAD_DELAY = 2  # Delay (in seconds) between requests

# Output settings: Save scraped data in CSV format
FEED_FORMAT = 'csv'
# FEED_URI = 'output.csv'  # Uncomment to specify path for saving the output

# Default request headers
DEFAULT_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
}

# Enable cookies (enabled by default)
COOKIES_ENABLED = True

# Downloader middlewares
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 1,
    # 'scrapy_playwright.middlewares.PlaywrightMiddleware': 800,

    # Add other middlewares as needed (e.g., rotating proxies)
}

# List of rotating proxies to use
ROTATING_PROXY_LIST = [
    'http://username:password@proxy.scraperapi.com:8001',
    'http://username:password@us-il.proxymesh.com:31280',
    'http://username:password@proxy.crawlera.com:8010',
]

# Playwright settings (for browser automation)
PLAYWRIGHT_BROWSER_TYPE = "chromium"  # Can also be "firefox" or "webkit"
PLAYWRIGHT_LAUNCH_OPTIONS = {
    'headless': False,  # Set to False to see the browser in action
}

# AutoThrottle settings for controlling the scraping speed
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 5  # Initial delay before sending requests
AUTOTHROTTLE_MAX_DELAY = 20  # Maximum delay in case of high latency
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0  # Target number of concurrent requests per domain
AUTOTHROTTLE_DEBUG = False  # Disable debugging info for AutoThrottle

# Respect robots.txt settings (set to False to ignore)
ROBOTSTXT_OBEY = False

# User-agent for crawling (optional)
# USER_AGENT = 'product_scraper (+http://www.yourdomain.com)'

# Maximum concurrent requests performed by Scrapy (default is 16)
# CONCURRENT_REQUESTS = 32  # Adjust as needed

# Spider middlewares (optional)
# SPIDER_MIDDLEWARES = {
#     'product_scraper.middlewares.ProductScraperSpiderMiddleware': 543,
# }

# Downloader middlewares (optional)
# DOWNLOADER_MIDDLEWARES = {
#     'product_scraper.middlewares.ProductScraperDownloaderMiddleware': 543,
# }

# Extensions settings (optional)
# EXTENSIONS = {
#     'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Item pipelines (optional)
# ITEM_PIPELINES = {
#     'product_scraper.pipelines.ProductScraperPipeline': 300,
# }

# HTTP Cache settings (optional, disabled by default)
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
