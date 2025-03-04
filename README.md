# **Web Scraper**

A Python script to extract product data (like names, prices, and links) from websites and save it as a CSV. While tailored for one site, it's flexible enough to adapt to others with small tweaks.

---

## **What It Does**
- Automates browsing with **Selenium**.
- Extracts data using **BeautifulSoup**.
- Saves the results in a neat **CSV file**.

---

## **Requirements**
- **Python 3.7+**
- **Chrome** and **Chromedriver**
- Python Libraries:
  - `selenium`
  - `bs4`
  - `pandas`
  - `lxml`

---

## **Quick Start**

1. **Clone the repo**:
   
   git clone https://github.com/patrick-fitzs/webScraper.git

2. **Install dependencies:**
   
   pip install -r requirements.txt

3. **Update the script**:
   Change the base_url to match your target website.
   Adjust the CSS selectors for the data fields you want to scrape.

4. **Run the script**:
   python webScraper.py

---

### **Notes**
Websites do differ so you’ll need to tweak selectors to match their structure.
Some sites use JavaScript for dynamic content—handle this with waits or longer delays.
Always respect a site’s terms of use when scraping.

