# import requests

# def main():
#     url = 'https://api.coles.com.au/customer/v1/coles/products/search?limit=20&q=Drinks&start=40&storeId=7716&type=SKU'
#     h = {
#     'Accept-Encoding': 'gzip'
#     ,'Connection': 'keep-alive'
#     ,'Accept': '*/*' 
#     ,'User-Agent': 'Shopmate/3.4.1 (iPhone; iOS 11.4.1; Scale/3.00)'
#     ,'X-Coles-API-Key': '046bc0d4-3854-481f-80dc-85f9e846503d'
#     ,'X-Coles-API-Secret': 'e6ab96ff-453b-45ba-a2be-ae8d7c12cadf'
#     ,'Accept-Language': 'en-AU;q=1'
#     }

#     r = requests.get(url, headers=h)

#     j = r.json()

#     results  = j['Results']

#     for res in results:
#         print(res)

# if __name__ == '__main__':
#     main()
    