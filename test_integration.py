import unittest
from DCP import Scraper
from selenium import webdriver
import json
import os

class ScraperTestCase(unittest.TestCase):

    def setUp(self):            
        self.driver=webdriver.Chrome('C:/Users/kinan/miniconda3/envs/DCP/chromedriver.exe')     


    def test_Output(self):

        book_info = Scraper(URL = "https://www.waterstones.com/campaign/special-editions")
        book_info.accept_cookies()
        book_info.get_links()
        book_info.get_data()

        for index in range(len(book_info.link_list)):
            #test data.json
             try: 
                with open(os.path.join('raw_data', str(book_info.isbn_list[index]), 'data.json')) as f: 
                    return json.load(f) 

             except ValueError as e: 
                print('invalid json: %s' % e) 
                return None

        for index in range(len(book_info.link_list)):
            #test img file
             try: 
                with open(os.path.join('raw_data', str(book_info.isbn_list[index]), str(book_info.isbn_list[index]), '.jpg')) as f: 
                    return f.verify() 

             except ValueError as e: 
                print('invalid jpg: %s' % e) 
                return None

unittest.main(argv=[''], verbosity=2, exit=False)