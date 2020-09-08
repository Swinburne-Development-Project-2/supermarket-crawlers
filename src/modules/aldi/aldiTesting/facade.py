import requests
from bs4 import BeautifulSoup
import csv
import os

class facade:

     def __init__(self) -> None:
        pass
     

     def scrawler(self, sourceCode) -> None:
        headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}
        source = requests.get(sourceCode, headers = headers)
        html = source.content 
        soup = BeautifulSoup(html, 'lxml')
        if (os.path.isfile('scrape.csv')):
            csv_file = open('scrape.csv', 'a')
            csv_writer = csv.writer(csv_file)
        else:
            csv_file = open('scrape.csv', 'w')
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['Category', 'Product Name', 'Price'])
        title = soup.find("title").text
        print(title)
        for categoryList in soup.find_all('div', class_="box m-text-image"):
            category = categoryList.find('div', class_="box--description--header").text
            print (category)
            try: 
                priceItem = categoryList.find('div', class_="box--price")
                itemValue = priceItem.find('span', class_="box--value").text
                itemDecimal = priceItem.find('span', class_="box--decimal").text
            except Exception as e:
                itemValue = None
                itemDecimal = None   
            if (itemValue == None): 
                price = 0
                print("Look up in store")
            else:
                price = itemValue + itemDecimal     
                print (price)

            csv_writer.writerow([title, category, price])
        csv_file.close()