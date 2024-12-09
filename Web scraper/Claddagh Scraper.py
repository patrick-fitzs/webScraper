"""
This is a web scraper used to extract product details
[Name, price, link]
and export to CSV for working on.
"""

from selenium import webdriver               # For browser automation
from selenium.webdriver import ChromeOptions # to configure options for selenium
from bs4 import BeautifulSoup                # for parsing HTML content
import pandas as pd                          # used to export to csv
import time                                  # Introduce delays so dynamic content has time to load

# Initialize Selenium WebDriver
options = ChromeOptions()                    # Create ChromeOptions object to configure browser settings
# options.add_argument("--headless")         # Run browser in headless mode (no visible browser window) # Commented out so you can see what page is being scrapped
driver = webdriver.Chrome(options=options)   # Initialize Chrome WebDriver with specified options

# Starting URL (base URL)
base_url = "https://www.claddaghrings.com/yellow-gold-claddagh-rings/" # This is the first page
product_data = []                                                      # This list stores product details

# Number of pages to scrape
last_page = 4               # This was determined manually

# Iterate through pages
for current_page in range(1, last_page + 1):   # Loop from page 1 to last
    # Construct the URL for the current page
    if current_page == 1:
        page_url = base_url                            # First page is formatted differently from rest in URL so modifications were made.
    else:
        page_url = f"{base_url}page/{current_page}/"   # Appended 'page/x

    print(f"Scraping page {current_page}: {page_url}") # Prints the page were currently scraping
    driver.get(page_url)                               # This loads the page in the browser

    # Allow the page to load completely
    time.sleep(3)

    # Parse the page content with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'lxml')  # Parse HTML source from Selenium to Beautifulsoup. This allows us to select specific elements
                                                               # without this, it's a long string of text
    # Find all product containers
    product_containers = soup.select("div.product-small.col")   # Select all product containers using CSS selectors
    if not product_containers:
        print(f"No products found on page {current_page}. Stopping.")
        break  # Exit loop, stop if no products are found and log a report

    # Extract product details
    for container in product_containers:
        try:
            # Extract product name, these classes were found through inspect in web browser
            name = container.select_one("div.title-wrapper p.woocommerce-loop-product__title").get_text(strip=True)
            # Extract product price
            price = container.select_one("div.price-wrapper span.woocommerce-Price-amount").get_text(strip=True)
            # Extract product link
            link = container.select_one("a").get("href")

            # Add this data to product_data list created earlier
            product_data.append({
                "Name": name,
                "Price": price,
                "Link": link
            })
        except Exception as e: # Handles any exceptions during the data extraction
            print(f"Error extracting product data on page {current_page}: {e}") # log as this error

# Quit Selenium
driver.quit()  # Close the browser and release resources

# Save results to a CSV file
if product_data:  # if product contains data
    df = pd.DataFrame(product_data) # convert the list of dictionaries to a Pandas DataFrame
    df.to_csv("Scraped-data-files/Claddaghrings-com.csv", index=False, encoding="utf-8-sig")
    print("\nDone! Data saved to Claddaghrings-com.csv.")
else:
    print("No product data scraped.")


# Happy scraping