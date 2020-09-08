from src.components.crawler import Crawler
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from urllib.request import urlopen
from time import sleep
import json
import datetime
import sys

class WooliesBaseCrawler(Crawler):

    def __init__(self):
        super().__init__()
        self.headers = self.get_next_header()
        self.proxies = self.get_next_proxy()
        self.driver = self.get_web_driver()

    def get_web_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(ChromeDriverManager().install())
        return driver

    def format_url(self, base, page):
        return base + str(page)

    def parse_html_page(self, url):
        self.driver.get(url)
        sleep(5)
        html = self.driver.page_source
        parsed_html = BeautifulSoup(html, 'html.parser')
        return parsed_html

    def get_items_on_page(self, html):
        items = []
        try:
            items = html.findAll(
                'div', {'class': 'shelfProductTile-information'}
            )
        except Exception as e:
            print("ERROR - get_items_on_page: ", e)
        return items
    
    def get_category_title(self, html):
        category = "NA"
        try:
            category = html.find('h1', {'class': 'tileList-title'}).text.strip()
        except Exception as e:
            print("ERROR - get_category_title: ", e)
        return category