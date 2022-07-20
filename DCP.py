
from pickle import FALSE, TRUE
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time


class Scraper:

    def __init__(self, URL):
        self.driver = webdriver.Chrome() 
        self.driver.get(URL)
        
    
    def accept_cookies(self):
        delay = 10
        accept_cookies_button = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')))
        accept_cookies_button.click()
         

    def scroll(self,rep):
        for i in range(rep):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)


    def infinite_scroll(self):    
        show_more_button = self.driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[3]/div[3]/div[3]/button')
        show_more_button.click()
        delay = 10
        x = TRUE
        while x == TRUE:
            try:
                time.sleep(2)
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div[3]/div[3]/button')))
                time.sleep(1)
                show_more_button.click()
            except:
                x = FALSE

    def get_links(self):
        book_container =self. driver.find_element(by=By.XPATH, value='//div[@class="search-results-list"]') # XPath corresponding to the Container
        book_list = book_container.find_elements(by=By.XPATH, value='./div')
        self.link_list = []

        for book_property in book_list:
            a_tag = book_property.find_element(by=By.TAG_NAME, value='a')
            link = a_tag.get_attribute('href')
            self.link_list.append(link)
        

    def get_text_data(self):
        self.price_list = []

        for URL in self.link_list:
            self.driver.get(URL)
            time.sleep(0.5)
            price = self.driver.find_element(by=By.XPATH, value='//b[@itemprop="price"]').text
            self.price_list.append(price)
            #print(price)




if __name__ == "__main__":
    book_info = Scraper(URL = "https://www.waterstones.com/campaign/special-editions")
    book_info.accept_cookies()
    book_info.scroll(rep=3)
    book_info.infinite_scroll()
    book_info.get_links()
    book_info.get_text_data()
    print(book_info.price_list)
