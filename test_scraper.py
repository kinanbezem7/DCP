import string
import unittest
from DCP import Scraper
from selenium import webdriver

class ScraperTestCase(unittest.TestCase):

    def setUp(self):            
        self.driver=webdriver.Chrome('C:/Users/kinan/miniconda3/envs/DCP/chromedriver.exe')     


    def test_Scraper(self):

        book_info = Scraper(URL = "https://www.waterstones.com/campaign/special-editions")
        book_info.accept_cookies()
        book_info.get_links()
        book_info.get_data()
        self.assertIsInstance(book_info.link_list[0], str)
        self.assertIsInstance(book_info.name_list[0], str)
        self.assertIsInstance(book_info.price_list[0], str, float)
        self.assertIsInstance(book_info.isbn_list[0], str)
