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
import sys

# Load env variables
load_dotenv()
email = os.getenv("NEWEGG_EMAIL")
pwd = os.getenv("NEWEGG_PWD")
cvv = int(os.getenv("CREDIT_CARD_CVV"))
mouse_x = int(os.getenv("CLOUDFLARE_X_COORD"))
mouse_y = int(os.getenv("CLOUDFLARE_Y_COORD"))

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

def check_botted():
    global mouse_x, mouse_y
    time.sleep(1)
    cloudflared = driver.find_elements(By.CSS_SELECTOR, ".page-404-text")
    humaned = driver.find_elements(By.XPATH, "//p[contains(text(), 'Human')]")
    time.sleep(2)
    while cloudflared:
        print("Cloudflared!")
        cloudflared = driver.find_elements(By.CSS_SELECTOR, ".page-404-text")
        pyautogui.moveTo(mouse_x, mouse_y, duration=1)
        pyautogui.click()
        time.sleep(3)
    while humaned:
        print("Humaned!")
        humaned = driver.find_elements(By.XPATH, "//p[contains(text(), 'Human')]")
        time.sleep(5)
    return

def relogin():
    global pwd
    pwd_input = driver.find_elements(By.ID, "labeled-input-password")
    if pwd_input:
        pwd_input[0].send_keys(pwd)
        pwd_login_btn = driver.find_element(By.CSS_SELECTOR, ".btn-orange")
        driver.execute_script("arguments[0].click();", pwd_login_btn)
        check_botted()
        return true

def login():
    global email, pwd
    driver.get("https://secure.newegg.com/login/signin")
    time.sleep(2)
    check_botted()

    sign_in_err_page = driver.find_elements(By.CSS_SELECTOR, ".empty-buttons")
    relogin_page = driver.find_elements(By.ID, "labeled-input-password")
    already_signed_in_page = driver.find_elements(By.CSS_SELECTOR, ".account-settings")
    if sign_in_err_page:
        refresh_btn = driver.find_element(By.CSS_SELECTOR, ".btn-orange")
        driver.execute_script("arguments[0].click();", refresh_btn)
        time.sleep(3)
    elif relogin_page: 
        relogin()
    elif already_signed_in_page:
        return
    else:
        email_input = driver.find_element(By.ID, "labeled-input-signEmail")
        email_input.send_keys(email)
        email_login_btn = driver.find_element(By.CSS_SELECTOR, ".btn-orange")
        driver.execute_script("arguments[0].click();", email_login_btn)
        check_botted()

        pwd_input = driver.find_element(By.ID, "labeled-input-password")
        pwd_input.send_keys(pwd)
        pwd_login_btn = driver.find_element(By.CSS_SELECTOR, ".btn-orange")
        driver.execute_script("arguments[0].click();", pwd_login_btn)
        check_botted()

def add_to_cart():
    url = sys.argv[1]
    driver.get(url)
    check_botted()

    add_to_cart_btn = driver.find_element(By.CSS_SELECTOR, ".btn-wide")
    driver.execute_script("arguments[0].click();", add_to_cart_btn)
    check_botted()
    print("Added item to cart!")

    driver.get("https://secure.newegg.com/shop/cart")
    time.sleep(2)
    check_botted()

def place_order():
    global cvv
    checkout_btn = driver.find_element(By.CSS_SELECTOR, ".btn-wide")
    driver.execute_script("arguments[0].click();", checkout_btn)
    time.sleep(2)

    relogin()

    cvv_input = driver.find_element(By.NAME, "cvvNumber")
    cvv_input.click()
    time.sleep(2)
    cvv_input.send_keys(cvv)

    confirm_pmt_method_btn = driver.find_elements(By.CSS_SELECTOR, ".checkout-step-action-done")
    if confirm_pmt_method_btn:
        driver.execute_script("arguments[0].click();", confirm_pmt_method_btn[0])
        time.sleep(1)

    place_order_btn = driver.find_element(By.ID, "btnCreditCard")
    driver.execute_script("arguments[0].click();", place_order_btn)
    time.sleep(5)
    # Get the current URL
    current_url = driver.current_url

    # Check if 'confirmation' is in the current URL
    if "confirmation" in current_url:
        print("Order has been placed!")
    else:
        print(f"Was not able to complete your order: {current_url}")

if len(sys.argv) > 1:
    login()
    add_to_cart()
    place_order()
else:
    print("No URL provided.")
