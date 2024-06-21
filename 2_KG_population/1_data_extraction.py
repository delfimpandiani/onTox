"""
Script: data_extraction.py

This script performs web scraping to extract information about symbols associated with global extremism from a specified URL. It assigns unique identifiers to each symbol and organizes the data into a structured JSON format.

Dependencies:
- selenium: For web scraping and interaction.
- BeautifulSoup: For parsing HTML content.
- Chrome WebDriver: Specific to Selenium for browser automation.

Usage:
1. Adjust `url_path` to point to the desired URL containing symbol information.
2. Execute the script to scrape data, assign IDs, and generate `ontox_dict.json`.

Outputs:
- ontox_dict.json: JSON file containing structured symbol data with assigned OnTox IDs.

"""

import re
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


def scrape_data(url_path):
    """
    Scrapes symbol data from the provided URL.

    Args:
    - url_path (str): URL of the webpage containing symbol information.

    Returns:
    - dict: Dictionary (`symbol_chunks`) of symbol details including title, description, image URL, ideologies, and locations.
    """
    def scroll_to_element(driver, element):
        driver.execute_script("arguments[0].scrollIntoView();", element)
        time.sleep(2)  # Adjust the sleep time as needed
    # Start a Selenium WebDriver session
    driver = webdriver.Chrome()  # You need to have Chrome WebDriver installed
    driver.get(url_path)
    # Wait for the page to load
    time.sleep(5)  # Adjust the sleep time as needed
    # Click "See more" repeatedly until it's not found or no more new content is loaded
    previous_page_source = driver.page_source
    attempts = 0
    max_attempts = 1000
    while True:
        try:
            see_more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'See More')]"))
            )
            scroll_to_element(driver, see_more_button)  # Ensure the button is in view
            see_more_button.click()
            print("Clicked 'See More' button.")
            time.sleep(5)  # Wait for new content to load

            # Check if new content has been loaded
            current_page_source = driver.page_source
            if current_page_source == previous_page_source:
                print("No new content loaded. Exiting loop.")
                break
            previous_page_source = current_page_source

            attempts += 1
            if attempts > max_attempts:  # Limit the number of attempts to avoid infinite loop
                print("Reached the maximum number of attempts. Exiting loop.")
                break

        except Exception as e:
            print(f"Exception occurred: {e}")
            print("No more 'See more' buttons found or another issue occurred.")
            break
    # Get the page source after all "See more" clicks
    page_source = driver.page_source
    driver.quit()
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')
    def extract_specific_html(soup):
        symbol_chunks = {}
        # Find all the divs with class MuiGrid-root
        symbol_divs = soup.find_all('div', class_='MuiGrid-root')
        for div in symbol_divs:
            print("Processing div...")
            # Extract Symbol record id
            symbol_record_id_tag = div.find('a', {'data-action-button-id': True})
            if symbol_record_id_tag:
                href = symbol_record_id_tag.get('href')
                if href:
                    record_id = href.split('recordId=')[1]
                    symbol_chunks[record_id] = {}
            # Extract title
            heading = div.find('h2', class_='sw-width-l')
            if heading:
                symbol_name = heading.text.strip()
                symbol_chunks[record_id]['Title'] = symbol_name
                # print(f"Symbol name: {symbol_name}")
            # Extract description
            description = div.find('div', class_='sw-width-s')
            if description:
                description_text = description.text.strip()
                # print(f"Description: {description_text}")
                symbol_chunks[record_id]['Description'] = description_text
            # Extract image URL
            image_tag = div.find('div', {'class': 'static-image'})
            if image_tag:
                style = image_tag.get('style')
                if style:
                    url_start = style.find('url(&quot;') + len('url(&quot;')
                    url_end = style.find('&quot;)', url_start)
                    url = style[url_start:url_end]
                    url_pattern = re.compile(r'url\("([^"]+)"\)')
                    match = url_pattern.search(url)
                    if match:
                        url = match.group(1)
                        symbol_chunks[record_id]['Image_URL'] = url
                    else:
                        symbol_chunks[record_id]['Image_URL'] = "No URL found in the string."
            # Extract Ideology
            ideologies = []
            ideology_container = soup.find('div', {'data-field-id': '_rhibbccj4'})
            if ideology_container:
                chips = ideology_container.find_all('div', {'class': 'MuiChip-root'})
                for chip in chips:
                    label = chip.find('span', {'class': 'MuiChip-labelMedium'})
                    if label:
                        ideologies.append(label.get_text(strip=True))
            symbol_chunks[record_id]['Ideology'] = ', '.join(ideologies)
            locations = []
            location_container = soup.find('div', {'data-field-id': '_o9572zxac'})
            if location_container:
                chips = location_container.find_all('div', {'class': 'MuiChip-root'})
                for chip in chips:
                    label = chip.find('span', {'class': 'MuiChip-labelMedium'})
                    if label:
                        locations.append(label.get_text(strip=True))
            symbol_chunks[record_id]['Location'] = ', '.join(locations)
        return symbol_chunks
    symbol_chunks = extract_specific_html(soup)
    # Save the extracted data to a JSON file
    # with open('gpahe.json', 'w') as json_file:
    #     json.dump(symbol_chunks, json_file, indent=4)

    # print(json.dumps(symbol_chunks, indent=4))
    return symbol_chunks


def create_ontox_dict(symbol_chunks):
    """
    Assigns unique OnTox IDs to symbol data and structures it into JSON format.

    Args:
    - symbol_chunks (dict): Dictionary of symbol data obtained from `scrape_data`.

    Returns:
    - dict: Dictionary (`transformed_dict`) structured with GPAHE IDs, OnTox IDs, titles, descriptions, image URLs, ideologies, and locations.
    """
    transformed_dict = {}
    ontox_id_counter = 1

    for gpahe_id, symbol_data in symbol_chunks.items():
        symbol_entry = {
            "GPAHE_ID": gpahe_id,
            "OnTox_ID": f"Symbol_{ontox_id_counter}",
            "Title": symbol_data["Title"],
            "Description": symbol_data["Description"],
            "Image_URL": symbol_data["Image_URL"],
            "Ideology": symbol_data["Ideology"],
            "Location": symbol_data["Location"]
        }
        transformed_dict[f"Symbol_{ontox_id_counter}"] = symbol_entry
        ontox_id_counter += 1
        
    # Write the transformed dictionary to ontox_dict.json
    with open('../data/ontox_dict.json', 'w', encoding='utf-8') as f:
        json.dump(transformed_dict, f, indent=2, ensure_ascii=False)

    return transformed_dict

def main():
    """
    Main execution function to scrape symbol data, assign IDs, and generate JSON output.
    """
    url_path = "https://symbols.globalextremism.org/embed/pages/2c9b18da-3f19-4944-ae4d-64a5ee3b56a4/blocks/list2"
    symbol_chunks = scrape_data(url_path)
    extracted_dict = create_ontox_dict(symbol_chunks)

if __name__ == "__main__":
    main()