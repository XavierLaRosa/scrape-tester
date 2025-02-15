from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import re

# Path to ChromeDriver
driver_path = r"C:\Users\xavie\OneDrive\Desktop\projects\web scraping\tools\chromedriver.exe"

# Path to Brave profile with Surfshark logged in
profile_path = r"C:\Users\xavie\AppData\Local\BraveSoftware\Brave-Browser\User Data\Default"

# Set Brave as the browser
options = webdriver.ChromeOptions()
options.binary_location = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
options.add_argument(f"user-data-dir={profile_path}")
options.add_argument("--profile-directory=Default")
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")

# Start WebDriver with Brave
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

# Navigate to Newegg query URL
url = "https://www.newegg.com/p/pl?N=100007709%20601469158"
driver.get(url)

pattern = re.compile(r"^Add .* to cart$", re.IGNORECASE)

def scrape_items():
    """Scrape in-stock items and return a list of titles."""
    time.sleep(5)  # Wait for the page to load
    items = driver.find_elements(By.CSS_SELECTOR, ".btn-mini")
    
    in_stock_items = []
    for item in items:
        title = item.get_attribute("title")
        if title and pattern.match(title):
            in_stock_items.append(title)
    
    return in_stock_items

# Continuous scraping loop with refresh
try:
    while True:
        in_stock_items = scrape_items()

        if in_stock_items:
            print("\n📦 In-Stock Items Found:\n")
            for title in in_stock_items:
                print(f"✅ {title}")
            break
        else:
            print("No in-stock items found. Refreshing in 10 seconds...\n")
            time.sleep(10)
            driver.refresh()
except KeyboardInterrupt:
    print("\nScript terminated by user.")
finally:
    driver.quit()
