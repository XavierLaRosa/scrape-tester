import requests
from bs4 import BeautifulSoup

url = "https://www.newegg.com/p/pl?N=100007709%204131%20601408875"

headers = {
    "referer": "https://www.newegg.com/p/pl?N=100007709%204131%20601408875",
    "sec-ch-ua": '"Not(A:Brand";v="99", "Brave";v="133", "Chromium";v="133")',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)
print(f"Status code: {response.status_code}")

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # Check for button texts
    buttons = soup.find_all(string=lambda text: text and "Add to cart" in text)
    
    if buttons:
        print("\nFound 'Add to cart' buttons:")
        for btn in buttons:
            parent = btn.find_parent()
            title = parent.get('title') if parent else None
            print(f"Text: {btn.strip()} | Tag: {parent.name} | Class: {parent.get('class')} | Title: {title}")
    else:
        print("\nNo 'Add to cart' buttons found in static HTML.")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")