import requests
from bs4 import BeautifulSoup
import csv
import os
import json
from datetime import datetime

class facade:

     def __init__(self) -> None:
        pass

     def scrawler(self, sourceCode) -> None:
        headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}
        source = requests.get(sourceCode, headers = headers)
        html = source.content 
        soup = BeautifulSoup(html, 'lxml')
        title = soup.find("title").text
        splitTitle = title.split('-')
        supName = splitTitle[1]
        category = splitTitle[0]
        sourcefile = 'data/' + category + '.csv'
        csv_file = open(sourcefile, 'w')
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['supermarket','category', 'productname', 'price', 'baseprice', 'generalurl', 'imageurl', 'viewdate'])
        for categoryList in soup.find_all('a', class_="box--wrapper ym-gl ym-g25"):
            print(supName)
            print(category)
            pName = categoryList.find('div', class_="box--description--header").text
            pName = pName.strip()
            generalUrl = categoryList['href']
            imageUrl = categoryList.find('img')['src']
            print (pName)
            print (generalUrl)
            print (imageUrl)
            viewdate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            priceItem = categoryList.find('div', class_="box--price")
            try: 
                itemDecimal = priceItem.find('span', class_="box--decimal").text
            except Exception as e:
                itemDecimal = 0  
            try:
                itemValue = priceItem.find('span', class_="box--value").text
            except Exception as e:
                itemValue = 0
            try:
                basePrice = priceItem.find('span', class_= "box--baseprice").text
            except Exception as e:
                 basePrice = 0
            price = itemValue + itemDecimal  
            csv_writer.writerow([supName, category, pName, price, basePrice, generalUrl, imageUrl, viewdate])
        csv_file.close()