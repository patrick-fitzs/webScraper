Web Scraper
A Python script to extract product data (like names, prices, and links) from websites and save it as a CSV. While tailored for one site, it's flexible enough to adapt to others with small tweaks.

What It Does
Automates browsing with Selenium.
Extracts data using BeautifulSoup.
Saves the results in a neat CSV.
Requirements
Python 3.7+, Chrome, and Chromedriver.
Libraries: selenium, bs4, pandas, lxml.
Quick Start
Clone the repo:
bash
Copy code
git clone https://github.com/<your-username>/webScraper.git
Install dependencies:
bash
Copy code
pip install -r requirements.txt
Update the base_url and CSS selectors in the script to match your target website.
Run it:
bash
Copy code
python webScraper.py
Notes
Websites differ; you’ll need to adjust selectors to match their structure.
Some sites use JavaScript for dynamic content—handle this with waits or longer delays.
Always respect a site's terms of use!
