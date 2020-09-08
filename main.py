import requests
from bs4 import BeautifulSoup
from src.components.scraper import Scraper

def main():
    scrape = Scraper()
    print(scrape.get_next_proxy());

if __name__ == '__main__':
    main()