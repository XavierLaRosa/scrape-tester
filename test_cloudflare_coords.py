from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import pyautogui

# SE: Path to ChromeDriver
# windows: r"C:\Users\xavie\OneDrive\Desktop\projects\web scraping\tools\chromedriver.exe"
# linux: r"/home/xvr-linux-mint/Desktop/projects/web-scraping/tools/chromedriver-linux64/chromedriver""
# macos: r"/Users/xavierlarosa/Desktop/Workspace/web scraping/tools/chromedriver-mac-arm64-brave-version-133.0.6943.98/chromedriver"
driver_path = r"/Users/xavierlarosa/Desktop/Workspace/web scraping/tools/chromedriver-mac-arm64-brave-version-133.0.6943.98/chromedriver"

# SE: Path to Brave profile with Surfshark logged in
# windows: r"C:\Users\xavie\AppData\Local\BraveSoftware\Brave-Browser\User Data\Default"
# linux: r"/home/xvr-linux-mint/.config/BraveSoftware/Brave-Browser/Default""
# macos: r"/Users/xavierlarosa/Library/Application Support/BraveSoftware/Brave-Browser/Default"
profile_path = r"/Users/xavierlarosa/Library/Application Support/BraveSoftware/Brave-Browser/Default"

# SE: Set Brave as the browser
# windows: r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
# linux: r"/opt/brave.com/brave/brave"
# macos: r"/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
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
# in stock items: https://www.newegg.com/p/pl?N=100007709%204131
# in stock RTX 4080: https://www.newegg.com/p/pl?N=100007709%20601408875%204131
# in stock RTX 5080: https://www.newegg.com/p/pl?N=100007709%20601469158%204131
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

