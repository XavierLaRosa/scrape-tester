from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import re
import discord
import os
from dotenv import load_dotenv
import asyncio
import pyautogui
import pyscreeze

# Load env variables
load_dotenv()
user_id = int(os.getenv("DISCORD_USER_ID"))
channel_id = int(os.getenv("DISCORD_CHANNEL_ID"))
token_id = os.getenv("DISCORD_BOT_TOKEN")
mouse_x = int(os.getenv("CLOUDFLARE_X_COORD"))
mouse_y = int(os.getenv("CLOUDFLARE_Y_COORD"))

# Setup discord bot
intents = discord.Intents.default()
client = discord.Client(intents=intents)
user_mention = f"<@{user_id}>"

# SE: Path to ChromeDriver
driver_path = r"C:\Users\xavie\OneDrive\Desktop\projects\web scraping\tools\chromedriver.exe"

# SE: Path to Brave profile with Surfshark logged in
profile_path = r"C:\Users\xavie\AppData\Local\BraveSoftware\Brave-Browser\User Data\Default"

# SE: Set Brave as the browser
options = webdriver.ChromeOptions()
options.binary_location = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
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

pattern = re.compile(r"^Add .* to cart$", re.IGNORECASE)
in_stock_items = []
isCloudflared = False # if cloudflare 404 page occurs

class Item:
        def __init__(self, title, product_link, img_title, img_src, price):
            self.title = title
            self.product_link = product_link
            self.img_title = img_title
            self.img_src = img_src
            self.price = price

async def scrape_items():
    """Scrape in-stock items and return a list of titles."""
    await asyncio.sleep(5)  # Wait for the page to load
    itemCells = driver.find_elements(By.CSS_SELECTOR, ".item-cell")

    
    for item in itemCells:
        # Get add to cart button
        cart_element = item.find_element(By.CSS_SELECTOR, ".btn-mini")

        # Get product hyperlink
        link_element = item.find_element(By.CSS_SELECTOR, ".item-title")
        product_link = link_element.get_attribute("href")

        # Get image source and title
        img_element = item.find_element(By.CSS_SELECTOR, ".item-img img")
        img_src = img_element.get_attribute("src")
        img_title = img_element.get_attribute("title")

        # Get current price
        price_dollars = item.find_element(By.CSS_SELECTOR, ".price-current strong").text
        price_cents = item.find_element(By.CSS_SELECTOR, ".price-current sup").text
        price = f"${price_dollars}{price_cents}"
        title = cart_element.get_attribute("title")
        if title and pattern.match(title):
            title = title.replace("Add ", "").replace(" to cart", "")[:50]
            productItem = Item(title, product_link, img_title, img_src, price)
            in_stock_items.append(productItem)
            print(in_stock_items)
    return

# Start discord connection
@client.event
async def on_ready():
    global isCloudflared, mouse_x, mouse_y
    await client.wait_until_ready()
    channel = client.get_channel(channel_id)  # Replace with your channel ID
    try:
        while True:
            await scrape_items()

            if in_stock_items:
                print("\n📦 In-Stock Items Found:\n")
                for item in in_stock_items:
                    print(f"✅ {item.img_title} {item.product_link}")

                pretty_list_of_items = "\n".join([f"✅ [link]({item.product_link}): {item.img_title}" for item in in_stock_items])
                message = f"{user_mention} new items found! {url}\n{pretty_list_of_items}"
                await channel.send(message)
                break
            else:
                botDetectionPage = driver.find_elements(By.CSS_SELECTOR, ".page-404-text")
                if botDetectionPage and not isCloudflared:
                    isCloudflared = True
                    message = f"{user_mention} you have been cloudflared!"
                    print("You have been cloudflared. Refreshing in 10 seconds...\n")
                    await channel.send(message)
                    pyautogui.moveTo(mouse_x, mouse_y, duration=5)
                    pyautogui.click()
                elif not botDetectionPage:
                    isCloudflared = False
                    print("No in-stock items found. Refreshing in 10 seconds...\n")
                await asyncio.sleep(10)
                driver.refresh()
    except KeyboardInterrupt:
        print("\nScript terminated by user.")
    finally:
        driver.quit()

client.run(token_id)