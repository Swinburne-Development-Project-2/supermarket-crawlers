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
        # eliminate '&' character
        modifyCategory = category.replace('&','')
        modifyCategory = modifyCategory.strip()
        #seperate the category
        listCategory = modifyCategory.split(" ")
        finalcategory = self.convertCategory(listCategory)
        sourcefile = 'data/' + finalcategory + '.csv'
        csv_file = open(sourcefile, 'w')
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['supermarket','category', 'product_name', 'product_id', 'price', 'cup_price', 'product_url', 'img_url', 'viewed_date'])
        num = 1
        for categoryList in soup.find_all('a', class_="box--wrapper ym-gl ym-g25"):
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
                basePrice = priceItem.find('span', class_= "box--baseprice").text
            except Exception as e:
                 basePrice = 0
            try: 
                itemDecimal = priceItem.find('span', class_="box--decimal").text
            except Exception as e:
                itemDecimal = 'c' 
            try:
                itemValue = priceItem.find('span', class_="box--value").text
            except Exception as e:
                itemValue = 0

            if itemDecimal == '':
                price = '0.' + str(itemValue)
            else:        
                price = str(itemValue) + itemDecimal  
            #The ID number
            num += 1
            productID = self.generateID(supName, category, pName, num)
            print (productID)
            
            csv_writer.writerow([supName, category, pName, productID, price, basePrice, generalUrl, imageUrl, viewdate])
        csv_file.close()

     def returnListLink(self):
        resourceList = []
        resourceList.append('https://www.aldi.com.au/en/groceries/baby/baby-food/')
        resourceList.append('https://www.aldi.com.au/en/groceries/beauty/')
        resourceList.append('https://www.aldi.com.au/en/groceries/liquor/beer-cider/')
        resourceList.append("https://www.aldi.com.au/en/groceries/liquor/champagne-sparkling/")
        resourceList.append('https://www.aldi.com.au/en/groceries/pantry/chocolate/')
        resourceList.append('https://www.aldi.com.au/en/groceries/pantry/coffee/')
        resourceList.append('https://www.aldi.com.au/en/groceries/fresh-produce/dairy-eggs/')
        resourceList.append('https://www.aldi.com.au/en/groceries/freezer/')
        resourceList.append('https://www.aldi.com.au/en/groceries/pantry/gluten-free/')
        resourceList.append('https://www.aldi.com.au/en/groceries/health/')
        resourceList.append('https://www.aldi.com.au/en/groceries/laundry-household/household/')
        resourceList.append('https://www.aldi.com.au/en/groceries/laundry-household/laundry/')
        resourceList.append('https://www.aldi.com.au/en/groceries/liquor/wine/')
        resourceList.append('https://www.aldi.com.au/en/groceries/baby/nappies-and-wipes/')
        resourceList.append('https://www.aldi.com.au/en/groceries/pantry/olive-oil/')
        resourceList.append('https://www.aldi.com.au/en/groceries/pantry/just-organic/')
        resourceList.append('https://www.aldi.com.au/en/groceries/liquor/spirits/')
        resourceList.append('https://www.aldi.com.au/en/groceries/super-savers/')
        return resourceList

     def convertCategory(self, listCategory):
        listLength = len(listCategory)
        if listLength == 2:
            finalcategory = listCategory[0] + "_" + listCategory[1]
        elif listLength == 3:
            finalcategory = listCategory[0] + "_" + listCategory[1] + "_" + listCategory[2]    
        else:
            finalcategory = listCategory[0]
        return finalcategory 

     def generateID(self, supermarket, category, product_name, number):
         subsupermarket = supermarket[1] + supermarket[2]
         subcategory = category[0] + category[1] 
         subname = product_name[0] + product_name[1]
         productid = subsupermarket + subcategory + subname
         strNum = str(number)
         finalproductID = productid.lower()  + strNum
         return finalproductID
    
  