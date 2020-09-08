import requests
from bs4 import BeautifulSoup
from src.components.crawler import Crawler

def main():
    crawl = Crawler()
    print(crawl.get_next_proxy());

if __name__ == '__main__':
    main()