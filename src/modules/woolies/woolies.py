from bs4 import BeautifulSoup as soup
from selenium import webdriver
from urllib.request import urlopen
from time import sleep
from .base import WooliesBaseCrawler
from .woolies_urls import CATEGORY_URLS
import json
import datetime
import sys

{
    "url": {
        "class": "shelfProductTile-imageWrapper",
        "base": "https://www.woolworths.com.au",
        "append": "/shop/productdetails/544762/primo-chicken-breast-thinly-sliced"
    }
}

class WooliesCrawler(WooliesBaseCrawler):

    def __init__(self):
        super().__init__()

    def scrapping(self, html):

        containers = self.get_items_on_page(html)
        category = self.get_category_title(html)
        
        print('Total items in this page: ' + str(len(containers)))
        print('')
        
        arr = []
        
        for container in containers:
            # get the product name
            product_name = container.find('h3', {'class':'shelfProductTile-description'}).text.strip()
            # initial product is available
            availability = True
            # get the date and time of the scrapping time
            date_now = datetime.datetime.now()        

            # check price and availability of each item
            if(container.find('div', {'class': 'shelfProductTile-cupPrice'})):
                price = container.find('div', {'class': 'shelfProductTile-cupPrice'}).text.strip()
            elif(container.find('span', {'class':'price-dollars'})):
                price_dollar = container.find('span',{'class':'price-dollars'})
                price_cent = container.find('span', {'class': 'price-cents'})
                price = '$' + price_dollar.text + '.' + price_cent.text
            else:
                price = 'Currently not in stock'
                availability = False

            obj = {
                "name": product_name,
                "price": price,
                "availability": availability,
                "datetime": date_now,
                "category": category,
                "pic": None
            }

            #return all the items in the page
            arr.append(obj)
        return arr, len(containers)
    
    # convert datetime format to fit json
    def myconverter(self, o):
        if isinstance(o, datetime.datetime):
            return o.__str__()

    def run(self):
        # contain full list details for woolies
        full_list = []
        seller = {
            "seller": {
                "name": "Woolsworth",
                "description": "Woolsworth Supermarket",
                "url": "https://www.woolsworth.com.au",
                "added_datetime": None
            }
        }
        full_list.append(seller)
        arr = []  # used to store every object

        # scrapping for each section selected in the list
        for base_url in CATEGORY_URLS:
            n_items = 1
            page_number = 1

            while(n_items != 0):
                url = self.format_url(base_url, page_number)
                print('Page ' + str(page_number) + ": " + url)

                html = self.parse_html_page(url)

                arrSinglePage, n_items = self.scrapping(html)

                for obj in arrSinglePage:
                    arr.append(obj)

                page_number = page_number + 1


        #https://stackoverflow.com/questions/1720421/how-do-i-concatenate-two-lists-in-python
        # add the products array to the full list
        products = {'products': arr}
        full_list.append(products)

        # write a json file on all items
        with open('wooliesData.json', 'w') as outfile:
            json.dump(full_list, outfile, default=self.myconverter)

        print(len(arr))