from bs4 import BeautifulSoup as soup
from selenium import webdriver
from urllib.request import urlopen
from time import sleep
from .base import WooliesBaseCrawler
from .woolies_urls import CATEGORY_URLS
import json
import datetime
import uuid
import sys
import csv
import re

SUPERMARKET = 'Woolworths Supermarket'

CSV_COLUMN_NAMES = [
    'id',
    'supermarket',
    'category',
    'product_name',
    'product_id',
    'price',
    'cup_price',
    'product_url',
    'img_url',
    'viewed_date',
    'ratings',
    'rating_count',
    'product_specials',
    'available_in_stock'
]

class WooliesCrawler(WooliesBaseCrawler):

    def __init__(self):
        super().__init__()
        self.csv_writer = None
        self.csv_file = None
        self.current_category = None

    def insert_item_to_csv(self, data):
        self.csv_writer.writerow(data)

    def process_fields_in_item(self, item):
        product_name = self.get_product_name(item)
        viewed_date = self.NOW
        product_url = self.get_product_url(item)
        img_url = self.get_product_img_url(item)
        ratings = self.get_product_ratings(item)
        rating_count = self.get_rating_count(item)
        product_specials = self.get_product_specials(item)
        cup_price = self.get_product_cup_price(item)
        price = self.get_product_price(item)
        available_in_stock = True if price else False
        product_id = self.get_product_id(img_url)

        return [str(uuid.uuid4()),
            SUPERMARKET, 
            self.current_category,
            product_name,
            product_id,
            price,
            cup_price,
            product_url,
            img_url,
            viewed_date,
            ratings,
            rating_count,
            product_specials,
            available_in_stock]

    def scrape_items_on_page(self, html):
        items = self.get_items_on_page(html)
        print('Total items in this page: {}\n'.format(len(items)))

        self.current_category = self.get_category_title(html)

        for item in items:
            data = self.process_fields_in_item(item)
            
            if len(data) > 0:
                self.insert_item_to_csv(data)

        return len(items)
    
    def initialise_csv_writer(self, url):
        category = url.replace(
            'https://www.woolworths.com.au/shop/browse/', '').replace(
                '?pageNumber=', '').replace(
                    '-', '_')
        if not self.csv_writer and not self.csv_file:
            csv_path = './src/modules/woolies/data/{}.csv'.format(category)
            self.csv_file = open(csv_path, 'w')
            self.csv_writer = csv.writer(self.csv_file)
            self.csv_writer.writerow(CSV_COLUMN_NAMES)

    def close_csv(self):
        if self.csv_file:
            self.csv_file.close()
            self.csv_file = None
            self.csv_writer = None

    def run(self):
        for base_url in CATEGORY_URLS:
            num_items_remaining = 1
            page_number = 1

            self.initialise_csv_writer(base_url)

            while(num_items_remaining != 0):
                url = self.format_url(base_url, page_number)
                print('Page ' + str(page_number) + ": " + url)

                html = self.parse_html_page(url)
                num_items_remaining = self.scrape_items_on_page(html)

                page_number = page_number + 1

            self.close_csv()