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
import boto3 
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy import inspect
from selenium.webdriver.chrome.options import Options



s3_client = boto3.client('s3')




try:
    os.mkdir('raw_data')
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
        options = Options()
        options.add_argument("--headless") 
        options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36")
        self.driver = webdriver.Chrome(options=options) 
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

    def initialise_database(self):
            DATABASE_TYPE = 'postgresql'
            DBAPI = 'psycopg2'
            HOST = 'dcp.c1vhfqtykqij.us-east-1.rds.amazonaws.com'
            USER = 'postgres'
            PASSWORD = 'Nazim79737?'
            DATABASE = 'postgres'
            PORT = 5432
            engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
            engine.connect()
            return engine

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

    def rescrape(self, link_list, save_to_local, save_to_rds, engine):
        tot_link_list = []
        new_link_list = []

        if save_to_rds == TRUE:
            inspector = inspect(engine)
            inspector.get_table_names()
            tot_link_list = pd.read_sql_table('special_edition', engine)
            tot_link_list = tot_link_list.loc[:,"link"]
            tot_link_list = tot_link_list.tolist()
            
            for element in link_list:
                if element in tot_link_list:
                    pass
                else: 
                    new_link_list.append(element)

        if save_to_local == TRUE and save_to_rds == FALSE:
            total_isbn_list = os.listdir("raw_data")
            for index in range(len(total_isbn_list)):
                f = open(os.path.join('raw_data', str(total_isbn_list[index]),'data.json'), 'r')
                data = json.load(f)
                url = data["link"]
                tot_link_list.append(url)
                

            for element in link_list:
                if element in tot_link_list:
                    pass
                else: 
                    new_link_list.append(element)
                
        return new_link_list



        
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

    def save_data_files(
        self, 
        link_list, 
        price_list, 
        name_list, 
        isbn_list, 
        id_list, 
        img_list, 
        save_to_rds, 
        save_to_s3_from_file, 
        save_to_local, 
        engine):

        """Method for saving the data and images gathered to their respective folders and json files"""
        
        book_dict_list = []
        

        for index in range(len(link_list)):
            book_dict_list.append({'ID': id_list[index], 'ISBN': isbn_list[index], 'Price': price_list[index], 'Name': name_list[index], 'link': link_list[index]})
            if save_to_local == TRUE:
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

                if save_to_s3_from_file == TRUE:
                    file_name_img = ['raw_data/', str(book_dict_list[index]['ISBN']), '/',  str(book_dict_list[index]['ISBN']), '.jpg' ]
                    file_name_img_output = [str(book_dict_list[index]['ISBN']),".jpg"]
                    file_name_json = ['raw_data/', str(book_dict_list[index]['ISBN']), '/', 'data.json' ]
                    file_name_json_output = [str(book_dict_list[index]['ISBN']),".json"]

                    s3_client.upload_file(''.join(file_name_img), 'dcprawdata', ''.join(file_name_img_output))
                    s3_client.upload_file(''.join(file_name_json), 'dcprawdata', ''.join(file_name_json_output))

        if save_to_rds == TRUE:
            df = pd.DataFrame(book_dict_list)
            df.to_sql('special_edition', engine, if_exists="replace")

    def save_to_s3(
        self,         
        link_list, 
        price_list, 
        name_list, 
        isbn_list, 
        id_list, 
        img_list):

        book_dict_list = []
        tot_img_list = []
        tot_json_list = []

        obj_list = []
        session = boto3.Session()
        s3h = session.resource('s3')
        bucket = s3h.Bucket('dcprawdata')
        for obj in bucket.objects.all():
            if obj.key.endswith('jpg'):
                tot_img_list.append(obj.key)
            elif obj.key.endswith('json'):
                tot_json_list.append(obj.key)
            obj_list.append(obj)

        if "raw_data/" not in obj_list:
            s3_client.put_object(Bucket='dcprawdata', Body='',Key='raw_data/')
        for index in range(len(link_list)):
            book_dict_list.append({'ID': id_list[index], 'ISBN': isbn_list[index], 'Price': price_list[index], 'Name': name_list[index], 'link': link_list[index]})
            image = requests.get(str(img_list[index]), stream=TRUE)
            key_img = ['raw_data/', str(book_dict_list[index]['ISBN']), '.jpg']
            key_json = ['raw_data/', str(book_dict_list[index]['ISBN']), '.json']
            if ''.join(key_img) not in tot_img_list: 
                bucket.upload_fileobj(image.raw, ''.join(key_img))
            if ''.join(key_json) not in tot_json_list: 
                json_object = book_dict_list[index]
                s3_client.put_object(Body=json.dumps(json_object), Bucket='dcprawdata', Key=''.join(key_json))


        # else:
        #     for index in range(len(link_list)):
        #         book_dict_list.append({'ID': id_list[index], 'ISBN': isbn_list[index], 'Price': price_list[index], 'Name': name_list[index], 'link': link_list[index]})
        #         image = requests.get(str(img_list[index]), stream=TRUE)
        #         key_img = ['raw_data/', str(book_dict_list[index]['ISBN']), '.jpg']
        #         key_json = ['raw_data/', str(book_dict_list[index]['ISBN']), '.json']
        #         if ''.join(key_img) not in tot_img_list: 
        #             bucket.upload_fileobj(image.raw, ''.join(key_img))
        #         if ''.join(key_json) not in tot_json_list: 
        #             json_object = book_dict_list[index]
        #             s3_client.put_object(Body=json.dumps(json_object), Bucket='dcprawdata', Key=''.join(key_json))



if __name__ == "__main__":
    save_to_rds = FALSE
    save_to_s3_from_file = FALSE 
    save_to_local = TRUE
    save_to_s3 = FALSE # Upload images to s3 Bucket

    #book_info = Scraper(URL = "https://www.waterstones.com/campaign/special-editions")
    book_info = Scraper(URL = "https://www.waterstones.com/campaign/summer")
    print("Accept cookies")
    book_info.accept_cookies()
    #book_info.scroll(rep=3)
    #book_info.infinite_scroll()
    print("get links")
    link_list = book_info.get_links()
    print("get engine")
    engine = book_info.initialise_database()
    print("save")
    if save_to_local == TRUE or save_to_rds == TRUE:
        link_list = book_info.rescrape(link_list, save_to_local, save_to_rds, engine)
    print("get data")
    price_list, name_list, isbn_list, id_list, img_list = book_info.get_data(link_list)
    print("save data")
    book_info.save_data_files(link_list, price_list, name_list, isbn_list, id_list, img_list, save_to_rds, save_to_s3_from_file, save_to_local, engine)
    if save_to_s3 == TRUE:
        book_info.save_to_s3(link_list, price_list, name_list, isbn_list, id_list, img_list)

    book_info.driver.close()




