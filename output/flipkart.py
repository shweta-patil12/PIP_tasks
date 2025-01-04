from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Initialize the WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode (no browser window)
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Function to scrape product data
def scrape_lipkart():
    # Define the base URL (Example: Lipkart homepage or category page)
    url = "https://www.flipkart.com/search?q=laptop"
    
    # Open the page
    driver.get(url)
    time.sleep(3)  # Wait for page to load

    # Scroll to load more products (if required)
    for _ in range(5):  # Scroll 5 times for more products
        driver.execute_script("window.scrollBy(0, 1000);")
        time.sleep(2)

    # Find all the product links (based on the class you provided)
    product_links = driver.find_elements(By.CSS_SELECTOR, 'a[data-test="product-title"]')

    # Check if any products are found
    if product_links:
        for link in product_links:
            product_name = link.text
            product_url = link.get_attribute('href')
            print(f"Product: {product_name}")
            print(f"Link: {product_url}")
            print('-' * 50)
    else:
        print("No products found.")
    
    # Optionally handle pagination if needed (depends on the site structure)
    # You might need to click the "Next" button, for example:
    try:
        next_button = driver.find_element(By.CSS_SELECTOR, 'a.pagination-next')
        if next_button:
            next_button.click()
            time.sleep(3)  # Wait for the next page to load
            scrape_lipkart()  # Recursively scrape next page
    except Exception as e:
        print("No more pages or error in pagination:", e)

# Scrape data
scrape_lipkart()

# Close the driver
driver.quit()
