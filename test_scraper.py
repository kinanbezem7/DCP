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
        link_list = book_info.get_links()
        price_list, name_list, isbn_list, id_list, img_list = book_info.get_data(link_list)
        self.assertIsInstance(link_list[0], str)
        self.assertIsInstance(name_list[0], str)
        self.assertIsInstance(price_list[0], str, float)
        self.assertIsInstance(isbn_list[0], str)


unittest.main(argv=[''], verbosity=2, exit=False)
