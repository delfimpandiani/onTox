import os
import json
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options

# Load the toxic symbols data from the JSON file
with open('ontox_data.json', 'r') as f:
    symbol_data = json.load(f)

# Function to download an image
def download_image(url, folder_path, img_name):
    try:
        img_data = requests.get(url).content
        with open(f"{folder_path}/{img_name}.jpg", 'wb') as img_file:
            img_file.write(img_data)
    except Exception as e:
        print(f"Could not download {url}. Error: {e}")

# Set up ChromeDriver (ensure chromedriver is in PATH or give full path)
chrome_options = Options()
chrome_options.add_argument('--headless')  # Run in headless mode for speed
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service('chromedriver'), options=chrome_options)

# Google Image Search URL template
search_url = "https://www.google.com/search?q={}&tbm=isch"

# Base folder to save images
base_folder = "collected_images"
if not os.path.exists(base_folder):
    os.makedirs(base_folder)

# Function to search Google and download images
def search_and_download_images(symbol, search_term, folder_path):
    driver.get(search_url.format(search_term))
    time.sleep(2)  # Give some time for the page to load

    # Scroll down to load more images
    for _ in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    # Parse page content
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    img_tags = soup.find_all('img', {'class': 'rg_i Q4LuWd'})

    # Create folder for the symbol if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Download the first 300 images
    img_urls = []
    for i, img_tag in enumerate(img_tags[:300]):
        try:
            img_url = img_tag['src'] if 'src' in img_tag.attrs else img_tag['data-src']
            img_urls.append(img_url)
            download_image(img_url, folder_path, f"{symbol}_{i}")
        except Exception as e:
            print(f"Error in getting image {i}: {e}")
    
    print(f"Downloaded {len(img_urls)} images for {symbol}")

# Iterate through symbols and perform search
for symbol, details in symbol_data.items():
    search_term = f"{details['Title']} {details['Ideology']} meme"
    folder_path = os.path.join(base_folder, symbol)
    print(f"Searching for {search_term}")
    search_and_download_images(symbol, search_term, folder_path)

# Close the browser after scraping
driver.quit()
