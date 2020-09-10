from src.components.crawler import Crawler
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from urllib.request import urlopen
from time import sleep
import json
import datetime
import sys

BASE_URL = 'https://www.woolworths.com.au'

class WooliesBaseCrawler(Crawler):

    def __init__(self):
        super().__init__()
        self.headers = self.get_next_header()
        self.proxies = self.get_next_proxy()
        self.driver = self.get_web_driver()

    def get_web_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--proxy-server={}'.format(self.proxies['https']))
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(ChromeDriverManager().install())
        return driver

    def format_url(self, base, page):
        return base + str(page)

    def parse_html_page(self, url):
        attempt = 0
        while (attempt != 3):
            try:
                self.driver.get(url)
                sleep(5)
                html = self.driver.page_source
                parsed_html = BeautifulSoup(html, 'html.parser')
            except Exception as e:
                self.rotate_ip_for_driver()
                sleep(5)
                print(e)
            attempt += 1
        return parsed_html

    def rotate_ip_for_driver(self):
        self.driver.quit()
        self.proxies = self.get_next_proxy()
        self.driver = self.get_web_driver()

    def get_items_on_page(self, html):
        items = []
        try:
            items = html.findAll(
                'div', {'class': 'shelfProductTile-content'}
            )
        except Exception as e:
            print("ERROR - get_items_on_page: {}".format(e))
        return items
    
    def get_category_title(self, html):
        category = None
        try:
            category = html.find('h1', {'class': 'browseContainer-title'}).text.strip()
        except Exception as e:
            print("ERROR - get_category_title: {}".format(e))
        return category

    def get_product_name(self, item_html):
        product_name = None
        try:
            product_name = item_html.find('header', 
                {'class':'shelfProductTile-description'}).text
            product_name = ' '.join(product_name.split())
        except Exception as e:
            print("ERROR - get_product_name: {}".format(e))
        return product_name

    def get_product_url(self, item_html):
        product_url = None
        try:
            product_url = item_html.find('a', 
                {'class':'shelfProductTile-imageWrapper'})['href']
            product_url = '{}{}'.format(BASE_URL, product_url)
        except Exception as e:
            print("ERROR - get_product_url: {}".format(e))
        return product_url

    def get_product_img_url(self, item_html):
        product_img_url = None
        try:
            product_img_url = item_html.find('img', 
                {'class':'shelfProductTile-image'})['src']
        except Exception as e:
            print("ERROR - get_product_img_url: {}".format(e))
        return product_img_url

    def get_product_ratings(self, item_html):
        product_ratings = None
        try:
            product_ratings = item_html.find('div', 
                {'class':'shelfProductTile-ratingBlock'}).find('span', 
                {'class':'sr-only'}).text.strip()
        except Exception as e:
            print("ERROR - get_product_ratings: {}".format(e))
        return product_ratings

    def get_rating_count(self, item_html):
        rating_count = 0
        try:
            rating_count = item_html.find('span', 
                {'class':'rating-count'}).text.strip().strip('()')
        except Exception as e:
            print("ERROR - get_rating_count: {}".format(e))
        return rating_count

    def get_product_specials(self, item_html):
        product_specials = None
        try:
            product_specials = item_html.find('div', 
                {'class':'shelfProductTagCenter'}).text.strip()
        except Exception as e:
            print("ERROR - get_product_specials: {}".format(e))
        return product_specials

    def get_product_cup_price(self, item_html):
        cup_price = None
        try:
            cup_price = item_html.find('div', 
                {'class':'shelfProductTile-cupPrice'}).text.strip()
        except Exception as e:
            print("ERROR - get_product_cup_price: {}".format(e))
        return cup_price

    def get_product_price(self, item_html):
        price = None
        try:
            dollar_amount = item_html.find('span', 
                {'class':'price-dollars'}).text.strip()
            cent_amount = item_html.find('span', 
                {'class':'price-cents'}).text.strip()
            price = '${}{}'.format(dollar_amount, cent_amount)
        except Exception as e:
            print("ERROR - get_product_price: {}".format(e))
        return price