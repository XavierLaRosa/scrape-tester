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
import subprocess

# Load env variables
load_dotenv()
email = os.getenv("NEWEGG_EMAIL")
pwd = os.getenv("NEWEGG_PWD")
cvv = int(os.getenv("CREDIT_CARD_CVV"))
user_id = int(os.getenv("DISCORD_USER_ID"))
channel_id = int(os.getenv("DISCORD_CHANNEL_ID"))
token_id = os.getenv("DISCORD_BOT_TOKEN")
mouse_x = int(os.getenv("CLOUDFLARE_X_COORD"))
mouse_y = int(os.getenv("CLOUDFLARE_Y_COORD"))
chrome_driver_path = rf"{os.getenv("CHROME_DRIVER_PATH")}"
brave_extensions_profile_path = rf"{os.getenv("BRAVE_EXTENSIONS_PROFILE_PATH")}"
brave_binary_path = rf"{os.getenv("BRAVE_BINARY_PATH")}"

# Local variables
in_stock_items = []
prioritized_items = ["INSPIRE", "PRIME", "Founders", "SOLID"]
url = "https://www.newegg.com/p/pl?N=100007709%20601469158%204131&PageSize=96"
bot_detection = 0
last_bot_detection_state = ""

# Setup discord bot
intents = discord.Intents.default()
client = discord.Client(intents=intents)
user_mention = f"<@{user_id}>"

# SE: Set Brave as the browser
options = webdriver.ChromeOptions()
options.binary_location = brave_binary_path
options.add_argument(f"user-data-dir={brave_extensions_profile_path}")
options.add_argument("--profile-directory=Default")
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# SE: Start WebDriver with Brave
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)

class Item:
        def __init__(self, product_link, product_label, price):
            self.product_link = product_link
            self.product_label = product_label
            self.price = price

async def check_page():
    global bot_detection, last_bot_detection_state
    await asyncio.sleep(2)
    current_url = driver.current_url
    cloudflared = driver.find_elements(By.CSS_SELECTOR, ".page-404-text")
    if "identity/signin" in current_url:
        if last_bot_detection_state != "signin":
            bot_detection = 0
        last_bot_detection_state = "signin"
        if bot_detection == 1:
            print("Asked to sign in....")
        bot_detection = bot_detection + 1
        await login()
        await check_page()
    elif "areyouahuman" in current_url:
        if last_bot_detection_state != "human":
            bot_detection = 0
        last_bot_detection_state = "human"
        if bot_detection == 1:
            print("Got humaned...")
        bot_detection = bot_detection + 1
        await asyncio.sleep(5)
        await check_page()
    elif cloudflared:
        if last_bot_detection_state != "cloudflare":
            bot_detection = 0
        last_bot_detection_state = "cloudflare"
        if bot_detection == 1:
            print("Got cloudflared...")
        bot_detection = bot_detection + 1
        pyautogui.moveTo(mouse_x, mouse_y, duration=1)
        pyautogui.click()
        await asyncio.sleep(3)
        await check_page()
    else:
        last_bot_detection_state = ""
        bot_detection = 0
        return
    
async def login():
    global email, pwd

    current_url = driver.current_url
    if "signin" not in current_url:
        driver.get("https://secure.newegg.com/login/signin")
        await asyncio.sleep(2)

    sign_in_err_page = driver.find_elements(By.CSS_SELECTOR, ".empty-buttons")
    email_input = driver.find_elements(By.ID, "labeled-input-signEmail")
    pwd_input = driver.find_elements(By.ID, "labeled-input-password")
    if sign_in_err_page:
        refresh_btn = driver.find_element(By.CSS_SELECTOR, ".btn-orange")
        driver.execute_script("arguments[0].click();", refresh_btn)
        await asyncio.sleep(2)
    if email_input:
        email_input[0].send_keys(email)
        email_login_btn = driver.find_element(By.CSS_SELECTOR, ".btn-orange")
        driver.execute_script("arguments[0].click();", email_login_btn)
        await asyncio.sleep(2)
    if pwd_input:
        pwd_input[0].send_keys(pwd)
        pwd_login_btn = driver.find_element(By.CSS_SELECTOR, ".btn-orange")
        driver.execute_script("arguments[0].click();", pwd_login_btn)
        await asyncio.sleep(2)

async def add_to_cart(url):
    driver.get(url)
    await check_page()

    add_to_cart_btn = driver.find_element(By.CSS_SELECTOR, ".btn-wide")
    driver.execute_script("arguments[0].click();", add_to_cart_btn)
    await check_page()
    print("Added item to cart!")

async def place_order():
    global cvv
    driver.get("https://secure.newegg.com/shop/cart")
    await asyncio.sleep(2)
    await check_page()

    checkout_btn = driver.find_element(By.CSS_SELECTOR, ".btn-wide")
    driver.execute_script("arguments[0].click();", checkout_btn)
    await asyncio.sleep(2)
    await check_page()

    cvv_input = driver.find_element(By.NAME, "cvvNumber")
    cvv_input.click()
    await asyncio.sleep(2)
    cvv_input.send_keys(cvv)

    confirm_pmt_method_btn = driver.find_elements(By.CSS_SELECTOR, ".checkout-step-action-done")
    if confirm_pmt_method_btn:
        driver.execute_script("arguments[0].click();", confirm_pmt_method_btn[0])
        await asyncio.sleep(1)

    # place_order_btn = driver.find_element(By.ID, "btnCreditCard")
    # driver.execute_script("arguments[0].click();", place_order_btn)
    # await check_page()
    # await asyncio.sleep(5)

    current_url = driver.current_url
    if "confirmation" in current_url:
        print("Order has been placed!")
    else:
        print(f"Was not able to complete your order")

async def scrape_items():
    await asyncio.sleep(2)  # Wait for the page to load
    items = driver.find_elements(By.CSS_SELECTOR, ".item-cell")
    
    for item in items:
        # Get product hyperlink
        link_element = item.find_element(By.CSS_SELECTOR, ".item-title")
        product_link = link_element.get_attribute("href")

        # Get product label
        img_element = item.find_element(By.CSS_SELECTOR, ".item-img img")
        product_label = img_element.get_attribute("title")

        # Get current price
        price_dollars = item.find_element(By.CSS_SELECTOR, ".price-current strong").text
        price_cents = item.find_element(By.CSS_SELECTOR, ".price-current sup").text
        price = f"${price_dollars}{price_cents}"
  
        for prioritized_item in prioritized_items:
            if prioritized_item in product_label:
                print(f"Found: {product_label}")
                await add_to_cart(product_link)
                await place_order()
                # need to fix right here, where if order is placed, it breaks outer for loop since not in main items list page anymore

        productItem = Item(product_link, product_label, price)
        in_stock_items.append(productItem)
    return

# Start discord connection
@client.event
async def on_ready():
    global mouse_x, mouse_y
    await client.wait_until_ready()
    channel = client.get_channel(channel_id)
    try:
        await login()
        await check_page()
        driver.get(url)
        await check_page()

        while True:
            await check_page()
            await scrape_items()

            if in_stock_items:
                DISCORD_MSSG_LIMIT = 1900
                pretty_list_of_items = "\n".join([f"✅ [LINK]({item.product_link}): {item.product_label[:50]}" for item in in_stock_items])
                base_message = f"{user_mention}\n**Newegg restocked {len(in_stock_items)} [items!]({url})** 🎉😄🥂🎉\n"
                print(f"\n📦 In-Stock Items Found:\n{pretty_list_of_items}")
                
                # Function to chunk the message
                def chunk_message(message, limit):
                    chunks = []
                    current_chunk = ""
                    for line in message.split("\n"):
                        if len(current_chunk) + len(line) + 1 > limit:
                            chunks.append(current_chunk)
                            current_chunk = ""
                        current_chunk += line + "\n"
                    if current_chunk:
                        chunks.append(current_chunk)
                    return chunks

                # Split the message into chunks if needed
                messages = chunk_message(pretty_list_of_items, DISCORD_MSSG_LIMIT - len(base_message))
                for i, chunk in enumerate(messages, start=1):
                    header = f"{base_message}(Part {i}/{len(messages)})\n" if len(messages) > 1 else base_message
                    await channel.send(header + chunk)
                break
            else:
                print("No in-stock items found 😢. Refreshing in 5 seconds ⌚...\n")
                await asyncio.sleep(5)
                driver.refresh()
    except KeyboardInterrupt:
        print("\nScript terminated by user.")
    finally:
        driver.quit()

client.run(token_id)