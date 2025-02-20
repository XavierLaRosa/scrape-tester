cd "Web Scraping"
python3 -m venv venv
source venv/bin/activate
cd scrape-tester
pip install selenium discord.py python-dotenv pyautogui pyscreeze panda Pillow audioop-lts

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
options.binary_location = r"/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"

# SE: Navigate to Newegg query URL
# in stock items: https://www.newegg.com/p/pl?N=100007709%204131&PageSize=96
# in stock RTX 4080: https://www.newegg.com/p/pl?N=100007709%20601408875%204131&PageSize=96
# in stock RTX 5080: https://www.newegg.com/p/pl?N=100007709%20601469158%204131&PageSize=96
url = "https://www.newegg.com/p/pl?N=100007709%20601469158%204131&PageSize=96"

DISCORD_BOT_TOKEN=
DISCORD_CHANNEL_ID=
DISCORD_USER_ID=
CLOUDFLARE_X_COORD=
CLOUDFLARE_Y_COORD=
NEWEGG_EMAIL=
NEWEGG_PWD=
CREDIT_CARD_CVV=


# potential newegg pages:
- identity/signin url
- cloudflare https://www.newegg.com/p/pl?N=100007709%20601469158%204131
- human
