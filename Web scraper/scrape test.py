import requests                                 # provides methods for sending HTTP GET and POST requests
from bs4 import BeautifulSoup                   # Works with parser to extract data from HTML, used with requests
from selenium import webdriver                  # selenium (open-source browser automation tool) allows web scraping from dynamic webpages that use JavaScript/ Also helps bypass CAPTCHA
from selenium.webdriver import ChromeOptions
import pandas as pd                             # used to export data into a file


# Generate 5 URLs of search results.
pages = ['https://sandbox.oxylabs.io/products?page=' + str(i) for i in range(1, 6)]

# Crawl all URLs and extract each product's URL.
product_urls = []
for page in pages:
    print('Crawling page', page)
    # get() function to send HTTP request, this is part1, get the HTML using requests
    response = requests.get(page)
    soup = BeautifulSoup(response.text, 'lxml')

    for product in soup.select('.product-card'):
        href = product.find('a').get('href')
        product_urls.append('https://sandbox.oxylabs.io' + href)

print('\nFound', len(product_urls), 'product URLs.')


# Initialise a Chrome browser without its GUI.
options = ChromeOptions()
options.add_argument('--headless=new')
driver = webdriver.Chrome(options=options)

# Scrape all product URLs and parse each product's data.
products = []
for i, url in enumerate(product_urls, 1):
    print('Scraping URL', {i}, len(product_urls), end='\r')
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'lxml')

    info = soup.select_one('.brand-wrapper')

    product_data = {
        'Title': soup.find('h2').get_text(),
        'Price': soup.select_one('.price').get_text(),
        'Availability': soup.select_one('.availability').get_text(),
        'Stars': len(soup.select('.star-rating > svg')),
        'Description': soup.select_one('.description').get_text(),
        'Genres': ', '.join([genre.get_text().strip() for genre in soup.select('.genre')]),
        'Developer': info.select_one('.brand.developer').get_text().replace('Developer:', '').strip() if info else None,
        'Platform': info.select_one('.game-platform').get_text() if info and info.select_one('.game-platform') else None,
        'Type': info.select('span')[-1].get_text().replace('Type:', '').strip() if info else None
    }
    # Append each product's data to a list.
    products.append(product_data)
driver.quit()

# Save results to a CSV file.
df = pd.DataFrame(products)
df.to_csv('Scraped-data-files/products.csv', index=False, encoding='utf-8')
print('\n\nDone! Products saved to a CSV file.')