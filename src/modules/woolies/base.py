from src.components.crawler import Crawler
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from urllib.request import urlopen
from time import sleep
import json
import datetime
import sys

class WooliesBaseCrawler(Crawler):

    def __init__(self):
        super().__init__()
        self.headers = self.get_headers()
        self.proxies = self.get_proxies()