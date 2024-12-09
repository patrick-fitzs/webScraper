"""
Scraper to extract property price, link, and full address from details page.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
from bs4 import BeautifulSoup
import pandas as pd
import time

# Initialize Selenium WebDriver
options = ChromeOptions()
# options.add_argument("--headless")  # Uncomment for headless mode
driver = webdriver.Chrome(options=options)

# Starting URL (base URL)
base_url = "https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=REGION%5E225&radius=3.0&searchLocation=Bromley%2C%20London&useLocationIdentifier=true&sortType=6&viewType=LIST&channel=RENT&index="
property_data = []  # This list stores property details

# Step 1: Scrape the main listing page (first 5 properties)
print(f"Scraping the first 5 properties from: {base_url}")
driver.get(base_url)

# Handle the cookies popup
try:
    time.sleep(3)  # Wait for the popup to load
    accept_cookies_button = driver.find_element(By.ID, "onetrust-accept-btn-handler")
    accept_cookies_button.click()
    print("Accepted cookies popup.")
except Exception as e:
    print("No cookies popup found or issue clicking it:", e)

# Allow time for dynamic content to load
time.sleep(5)

# Parse the page content
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Find all property containers
property_containers = soup.select("div.PropertyCard_propertyCardContainerWrapper__mcK1Z")
print(f"Found {len(property_containers)} property containers.")

# Extract details for the first 5 properties
for i, container in enumerate(property_containers[:5]):  # Process only the first 5
    try:
        # Extract property price
        price_tag = container.select_one("div.PropertyPrice_price__VL65t")
        price = price_tag.get_text(strip=True) if price_tag else "No price available"

        # Extract property link
        link_tag = container.select_one("a.propertyCard-link")
        link = f"https://www.rightmove.co.uk{link_tag['href']}" if link_tag else "No link available"

        # Add to data list (Address to be fetched later)
        property_data.append({
            "Price": price,
            "Link": link,
            "Address": "To be fetched"
        })
    except Exception as e:
        print(f"Error extracting data for property {i + 1}: {e}")

# Step 2: Visit each property link and extract the full address
for property in property_data:
    if property["Link"] != "No link available":
        try:
            driver.get(property["Link"])
            time.sleep(5)  # Allow the details page to load

            # Parse the property details page
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Extract full address from the h1 tag with class 'streetAddress'
            address_tag = soup.select_one("h1.streetAddress")
            address = address_tag.get_text(strip=True) if address_tag else "No address found"

            # Update the property data with the fetched address
            property["Address"] = address
            print(f"Fetched Address: {address} for Link: {property['Link']}")
        except Exception as e:
            print(f"Error fetching address from {property['Link']}: {e}")

# Quit Selenium
driver.quit()

# Save to CSV
if property_data:
    df = pd.DataFrame(property_data)
    df.to_csv("Rightmove-First-5-Properties.csv", index=False, encoding="utf-8-sig")
    print("\nDone! Data saved to Rightmove-First-5-Properties.csv.")
else:
    print("No property data scraped.")
