from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import pyautogui

# SE: Path to ChromeDriver
driver_path = r"/Users/xavierlarosa/Desktop/Workspace/web scraping/tools/chromedriver-mac-arm64-brave-version-133.0.6943.98/chromedriver"

# SE: Path to Brave profile with Surfshark logged in
profile_path = r"/Users/xavierlarosa/Library/Application Support/BraveSoftware/Brave-Browser/Default"

# SE: Set Brave as the browser
options = webdriver.ChromeOptions()
options.binary_location = r"/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
options.add_argument(f"user-data-dir={profile_path}")
options.add_argument("--profile-directory=Default")
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# SE: Start WebDriver with Brave
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

# SE: Navigate to Newegg query URL
url = "https://www.newegg.com/p/pl?N=100007709%20601469158%204131"
driver.get(url)

try:
    print("Move the mouse to the desired location within 5 seconds...")
    time.sleep(15)  # Gives you time to place the mouse
    x, y = pyautogui.position()
    print(f"Mouse position: X={x}, Y={y}")
except KeyboardInterrupt:
    print("\nScript terminated by user.")
finally:
    driver.quit()

