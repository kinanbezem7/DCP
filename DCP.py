
from pickle import FALSE, TRUE
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time



URL = "https://www.waterstones.com/campaign/special-editions"
driver = webdriver.Chrome() 
driver.get(URL)
#time.sleep(2) 
#accept_cookies_button = driver.find_element(by=By.XPATH, value='//*[@id="onetrust-accept-btn-handler"]')
#accept_cookies_button.click()
#driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")





class Scraper:
    
    def accept_cookies(self, driver):
        delay = 10
        accept_cookies_button = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')))
        #accept_cookies_button = driver.find_element(by=By.XPATH, value='//*[@id="onetrust-accept-btn-handler"]')
        accept_cookies_button.click()
         

    def scroll(self, driver):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        #show_more_button = driver.find_element(by=By.CLASS_NAME, value='button button-teal')
        show_more_button = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[3]/div[3]/div[3]/button')
        show_more_button.click()
        delay = 10
        x = TRUE
        while x == TRUE:
            try:
                time.sleep(2)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div[3]/div[3]/button')))
                time.sleep(1)
                show_more_button.click()
            except:
                x = FALSE

    def get_links(self, driver):
        book_container = driver.find_element(by=By.XPATH, value='//div[@class="search-results-list"]') # XPath corresponding to the Container
        book_list = book_container.find_elements(by=By.XPATH, value='./div')
        link_list = []

        for book_property in book_list:
            a_tag = book_property.find_element(by=By.TAG_NAME, value='a')
            link = a_tag.get_attribute('href')
            link_list.append(link)
        return link_list

    def get_text_data(self,driver, link_list):
    #     for URL in link_list:
        URL = link_list[1]
        driver.get(URL)
        time.sleep(2)
        price = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[2]/div[2]/section[1]/div[2]/div[2]/div/div/div/div[1]/div/b[2]').text
        print(price)




if __name__ == "__main__":
    book_info = Scraper()
    book_info.accept_cookies(driver)
    #book_info.scroll(driver)
    link_list = book_info.get_links(driver)
    print(len(link_list))
    print(link_list[1])

    book_info.get_text_data(driver, link_list)
