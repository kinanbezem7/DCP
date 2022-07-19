from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def load_and_accept_cookies() -> webdriver.Chrome:
    '''
    Open Zoopla and accept the cookies
    
    Returns
    -------
    driver: webdriver.Chrome
        This driver is already in the Zoopla webpage
    '''
    driver = webdriver.Chrome() 
    URL = "https://www.zoopla.co.uk/new-homes/property/london/?q=London&results_sort=newest_listings&search_source=new-homes&page_size=25&pn=1&view_type=list"
    driver.get(URL)
    time.sleep(3) 
    try:
        driver.switch_to_frame('gdpr-consent-notice') # This is the id of the frame
        accept_cookies_button = driver.find_elementh(by=By.XPATH, value='//*[@id="save"]')
        accept_cookies_button.click()
        time.sleep(1)
    except AttributeError: # If you have the latest version of Selenium, the code above won't run because the "switch_to_frame" is deprecated
        driver.switch_to.frame('gdpr-consent-notice') # This is the id of the frame
        accept_cookies_button = driver.find_element(by=By.XPATH, value='//*[@id="save"]')
        accept_cookies_button.click()
        time.sleep(1)

    except:
        pass

    return driver 


driver = load_and_accept_cookies() # In case it works, driver should be in the Zoopla webpage with the cookies button clicked
prop_container = driver.find_element(by=By.XPATH, value='//div[@class="css-1itfubx eid9civ0"]') # XPath corresponding to the Container
prop_list = prop_container.find_elements(by=By.XPATH, value='./div')
link_list = []

for house_property in prop_list:
    a_tag = house_property.find_element(by=By.TAG_NAME, value='a')
    link = a_tag.get_attribute('href')
    link_list.append(link)
    
print(f'There are {len(link_list)} properties in this page')
print(link_list)

