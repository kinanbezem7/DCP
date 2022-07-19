from selenium import webdriver
from selenium.webdriver.common.by import By
import time


# class Scraper:
driver = webdriver.Chrome() 
URL = "https://www.merlinarchery.co.uk/bows/traditional-bows/horse-bows.html"
driver.get(URL)
time.sleep(2) 


prop_container = driver.find_element(by=By.XPATH, value='//*[@id="m-navigation-product-list-wrapper"]/div[2]/ol') # XPath corresponding to the Container

prop_list = prop_container.find_elements(by=By.XPATH, value='./li')
link_list = []
price_list = []

for horse_bow in prop_list:
    a_tag = horse_bow.find_element(by=By.TAG_NAME, value='a')
    link = a_tag.get_attribute('href')
    link_list.append(link)

    span_tag = horse_bow.find_element(by=By.CLASS_NAME, value='price-wrapper')
    price = span_tag.get_attribute('data-price-amount')
    price_list.append(price)
    

print(f'There are {len(link_list)} bows in this page')
print(link_list)
print(price_list)
