import requests
from bs4 import BeautifulSoup
from src.components.crawler import Crawler
from src.modules.woolies.woolies import WooliesCrawler

def main():
    crawler = WooliesCrawler()
    print(crawler.run());

if __name__ == '__main__':
    main()