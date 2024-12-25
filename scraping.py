from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime
import os
import re
import email_automator

url = 'https://www.finewineandgoodspirits.com/'
if not os.path.isdir("output"):
    os.mkdir("output")
output_file = "valid_stores_" + str(datetime.now().date()) + ".txt"
output_file_name = os.path.join("output", output_file)
TEST = False
MAX_ZIPCODE = '19103'


def open_page(url):
    # Set up web browser
    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    if TEST:
        driver = webdriver.Chrome()

    else:
        driver = webdriver.Chrome(options = options)
    
    # Go to main page of site and pass the age question
    driver.get(url)
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label = 'Yes, Enter into the site']")))
    yes_button = driver.find_element(By.XPATH, "//button[@aria-label = 'Yes, Enter into the site']")
    yes_button.click()

    return driver


def search_results(url, search):
    
    try:
        driver = open_page(url)
        wait = WebDriverWait(driver, 3)

        # Enter value into search box
        search_box = driver.find_element(By.XPATH, "//input[@type = 'text']")
        search_button = driver.find_element(By.XPATH, "//button[@aria-label = 'Search Icon']")
        search_box.send_keys(search)
        search_button.click()
        wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'product-card-link')))

        # Parse page to get all items on that page
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        found = (soup.find_all('a', {'class': 'product-card-link'}))
        driver.quit()
        return {href.get('aria-label'): href.get('href') for href in found}
    
    except:
        error_writing()


def error_writing():
    with open(output_file_name, 'a') as file:
        file.write("-" * 20)
        file.write("\n")
        file.write("Not found on website\n")
        file.write("-" * 20)
        file.write("\n")
    

# Creates urls out of the search result's hrefs
def url_constructor(url, search_results):
    if search_results is not None:
        for result in search_results.keys():
            search_facts(result, url + search_results[result])


def search_facts(search, url):
    with open(output_file_name, 'a') as file:
        file.write("\n" + search + "\n\n")
        try:
            driver = open_page(url)
            avail_button = driver.find_element(By.XPATH, '/html/body/div[1]/main/section[2]/div/div/div[2]/div[3]/div/button')
            avail_button.click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/header/section/div[3]/div[1]/section[1]/div/section/section/div[3]/div[3]/div/div/div/div/div[2]/button[1]')))
            pick_up_button = driver.find_element(By.XPATH, '/html/body/div[1]/header/section/div[3]/div[1]/section[1]/div/section/section/div[3]/div[3]/div/div/div/div/div[2]/button[1]')
            pick_up_button.click()
            zipcode_bar = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/header/section/div[3]/div[3]/div/div/div[3]/div[1]/div[1]/input")))
            zipcode_button = driver.find_element(By.XPATH, '/html/body/div[1]/header/section/div[3]/div[3]/div/div/div[3]/div[1]/div[1]/span[2]/button')
            zipcode_bar.click()
            zipcode_bar.send_keys(MAX_ZIPCODE)
            zipcode_button.click()
            WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'storeCardModal_content')))

            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            store_cards = soup.find_all('div', class_='storeCardModal_content')

            for card in store_cards:
                # Check if the 'icon-checkmark' span exists within this card (indicating the store is available)
                if card.find('span', class_='icon-checkmark'):

                    # Check if direction is within the desired range
                    location_text = card.find('div', class_='direction').find('p', class_='paragraph').text
                    match = re.search(r'(\d+(\.\d+)?)\s*miles', location_text)

                    if match:
                        distance = float(match.group(1))

                        # CHANGE THIS IF YOU WANT TO ADJUST YOUR DISTANCE RANGE
                        if distance < 50.0:

                            # Find the address of this store
                            address = card.find('div', class_='address')
                            if address:
                                file.write(f"Store is located {distance} miles away.\n")
            
                                store_name = address.find('h4').text
                                street_address = address.find_all('p')[0].text
                                city_state_zip = address.find_all('p')[1].text
                                # hyper_link = location_text.find('a', href = True, text = "Get Directions") get the hyperlink at some point
                                file.write(f"Store Name: {store_name}\n")
                                file.write(f"Street Address: {street_address}\n")
                                file.write(f"City/State/Zip: {city_state_zip}\n")
                                # file.write(f"Google Maps: {hyper_link['href']}\n") 
                                file.write("-" * 20)
                                file.write("\n")
            driver.quit()

        except:
            file.write("-" * 20)
            file.write("\n")
            file.write("Not found in any of the stores\n")
            file.write("-" * 20)
            file.write("\n")

        
def main():
    with open('input_liquors.txt', "r") as file:
        inputs = file.readlines()
        for i in inputs:
            url_constructor(url, (search_results(url, i)))

    with open(output_file_name, "r") as f:
        body = f.read()

    if TEST:
        recipient = "zachkaufman36@gmail.com"

    else:
        recipient = "maxkaufman@ymail.com"
        
    email_automator.send_email(body, recipient)


if __name__ == '__main__':
    main()