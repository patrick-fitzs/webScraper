import time
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

# Initialize Selenium WebDriver
options = webdriver.ChromeOptions()

driver = webdriver.Chrome(options=options)

# List of pages to scrape
pages = ["https://www.scan.co.uk/shop/computer-hardware/gpu-nvidia-gaming/all"]

# Initialize list to store product details
products = []

# Step 1: Scrape product details (name, price, URL) from the main page
for page in pages:
    print(f"Crawling {page}")
    driver.get(page)  # Load the page with Selenium
    time.sleep(3)  # Allow JavaScript content to fully load

    # Use BeautifulSoup to parse the page
    soup = BeautifulSoup(driver.page_source, "lxml")

    # Find all product elements
    product_elements = soup.select("ul.product-group li")

    for product in product_elements:
        try:
            # Extract product URL
            url_tag = product.find("a", href=True)
            product_url = f"https://www.scan.co.uk{url_tag['href']}" if url_tag else None

            # Extract product title (name)
            title_tag = product.find("span", class_="description")
            title = title_tag.get_text(strip=True) if title_tag else None

            # Extract product price
            price_tag = product.select_one("span.price")
            if price_tag:
                price = ''.join([text.strip() for text in price_tag.stripped_strings])
            else:
                price = None

            # Append to products list
            if product_url and title:
                products.append({
                    "Title": title,
                    "Price": price,
                    "URL": product_url
                })

        except Exception as e:
            print(f"Error scraping product: {e}")


# Quit the WebDriver
driver.quit()

# Step 2: Output results
# Convert the product data to a DataFrame
df = pd.DataFrame(products)

# Save to CSV for review
df.to_csv("Scraped-data-files/GPUs.csv", index=False, encoding="utf-8-sig")

print("Scraping complete. Product details saved to 'test.csv'.")
