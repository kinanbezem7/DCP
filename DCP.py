from pickle import FALSE, TRUE
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import uuid
import os
import json
import requests





try:
    os.mkdir('raw_data ')
except FileExistsError:
    print("Directory already exists")

class Scraper:
    """  
    Scraper class to get text and image data from waterstones website

    Attributes:
        URL (str): URL to the book list you want to extract data from i.e. "special editions"
    """

    def __init__(self, URL):
        '''
        See help(Scraper) for accurate signature
        '''
        self.driver = webdriver.Chrome() 
        self.driver.get(URL)
        
    
    def accept_cookies(self):
        """ 
        Method for pressing the accept cookies button at the bottom of the page
        """
        delay = 10
        accept_cookies_button = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')))
        accept_cookies_button.click()
         

    def scroll(self,rep):
        """ 
        Method for scrolling to the bottom of the page to load more books
        """
        for i in range(rep):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)


    def infinite_scroll(self):    
        """ 
        Method for infitely scrolling to the bottom of the list by pressing the "load more" button and scrolling. 
        This is used in order to load all of the books in the list
        """
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
        """ 
        Method for getting the links of all the books in the loaded list 

        Returns:
            link_list (list): list of the URL's for all the listed books
        """
        book_container =self. driver.find_element(by=By.XPATH, value='//div[@class="search-results-list"]') # XPath corresponding to the Container
        book_list = book_container.find_elements(by=By.XPATH, value='./div')
        link_list = []

        for book_property in book_list:
            a_tag = book_property.find_element(by=By.TAG_NAME, value='a')
            link = a_tag.get_attribute('href')
            link_list.append(link)

        return link_list
        
    def get_data(self, link_list):
        """ 
        Method for extracting image and text data for each books. This method will load each book individually, extract the text data and download their respective images. 

        Retruns:
            price_list (list): list of book prices
            name_list (list): List of book names 
            isbn_list (list): List of the ISBN numbers 
            id_list (list): List UUID4 reference for each of the books
            img_list (list): List SRC links for the main image of each book  
        """
        price_list = []
        name_list = []
        isbn_list = []
        id_list = []        
        img_list = []

        for URL in link_list:
            self.driver.get(URL)
            time.sleep(0.5)
            #Get text data
            price = self.driver.find_element(by=By.XPATH, value='//b[@itemprop="price"]').text
            price_list.append(str(price))
            name = self.driver.find_element(by=By.XPATH, value='//span[@class="book-title"]').text
            name_list.append(name)
            isbn = self.driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[2]/div[2]/section[2]/div[2]/div/div/p/i[2]/span').text
            isbn_list.append(isbn)
            book_id = str(uuid.uuid4())
            id_list.append(book_id)
            #Get image data
            img_container =self.driver.find_element(by=By.XPATH, value='//div[@class="main-container"]') # XPath corresponding to the Container
            img_tag = img_container.find_element(by=By.XPATH, value='.//img[@itemprop="image"]')
            src = img_tag.get_attribute('src')
            img_list.append(src)
        return price_list, name_list, isbn_list, id_list, img_list

    def save_data_files(self, link_list, price_list, name_list, isbn_list, id_list, img_list):

        """Method for saving the data and images gathered to their respective folders and json files"""
        
        book_dict_list = []

        for index in range(len(link_list)):
            book_dict_list.append({'ID': id_list[index], 'ISBN': isbn_list[index], 'Price': price_list[index], 'Name': name_list[index]})

            try:
                path = ['raw_data/', str(book_dict_list[index]['ISBN'])]
                os.mkdir(''.join(path))
                
            except FileExistsError:
                print("Directory already exists")


            with open(os.path.join('raw_data', str(book_dict_list[index]['ISBN']),'data.json'), 'w') as fp:
                json.dump(book_dict_list[index], fp)

            path = ['raw_data/', str(book_dict_list[index]['ISBN']), '/',  str(book_dict_list[index]['ISBN']), '.jpg' ]
            image = requests.get(str(img_list[index])).content
            with open(''.join(path), "wb") as outimage:
                outimage.write(image)


if __name__ == "__main__":
    book_info = Scraper(URL = "https://www.waterstones.com/campaign/special-editions")
    book_info.accept_cookies()
    #book_info.scroll(rep=3)
    #book_info.infinite_scroll()
    link_list = book_info.get_links()
    price_list, name_list, isbn_list, id_list, img_list = book_info.get_data(link_list)
    book_info.save_data_files(link_list, price_list, name_list, isbn_list, id_list, img_list)



"""
    book_dict_list = []


     for index in range(len(book_info.link_list)):
        book_dict_list.append({'ID': book_info.id_list[index], 'ISBN': book_info.isbn_list[index], 'Price': book_info.price_list[index], 'Name': book_info.name_list[index]})
        try:
            os.mkdir(os.path.join('raw_data', str(book_dict_list[index]['ISBN'])))

        except FileExistsError:
            print("Directory already exists")

        with open(os.path.join('raw_data', str(book_dict_list[index]['ISBN']),'data.json'), 'w') as fp:
            json.dump(book_dict_list[index], fp)

        path = ['raw_data/', str(book_dict_list[index]['ISBN']), '/',  str(book_dict_list[index]['ISBN']), '.jpg' ]
        image = requests.get(str(book_info.img_list[index])).content
        with open(''.join(path), "wb") as outimage:
            outimage.write(image) """




