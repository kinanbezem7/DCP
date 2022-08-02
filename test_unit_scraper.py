import unittest
from DCP import Scraper
from selenium import webdriver


class ScraperTestCase(unittest.TestCase, Scraper):

    def setUp(self):            
        self.driver=webdriver.Chrome('C:/Users/kinan/miniconda3/envs/DCP/chromedriver.exe')     
        #self.accept_cookies()

    def test_Scraper(self):

        expected_value = []
        price_list, name_list, isbn_list, id_list, img_list = self.get_data(link_list=['https://www.waterstones.com/book/nightcrawling/leila-mottley/9781526653710', 'https://www.waterstones.com/book/the-house-of-fortune/jessie-burton/2928377071592'])
        self.assertEqual(type(price_list), list)
        self.assertEqual(type(name_list), list)
        self.assertEqual(type(isbn_list), list)
        self.assertEqual(type(id_list), list)
        self.assertEqual(type(img_list), list)
        self.assertEqual(type(price_list[0]), str)
        self.assertEqual(type(name_list[0]), str)
        self.assertEqual(type(isbn_list[0]), str)
        self.assertEqual(type(id_list[0]), str)
        self.assertEqual(type(img_list[0]), str)


unittest.main(argv=[''], verbosity=2, exit=False)