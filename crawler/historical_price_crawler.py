'''
This file uses selenium chromedriver to parse historical prices from nasdaq.com
Data is stored in ../data/historical_price/.

'''
import urllib.request
from html.parser import HTMLParser
import requests
import json
import pprint
import random
import datetime
import json
import time
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import os
import time
import shutil
import csv
import random

'''
all stocks in nasdaq
https://www.nasdaq.com/market-activity/stocks/screener

'''
SYMBOL_FILE = '../data/symbol/nasdaq.csv'
HISTORICAL_PREFIX = 'http://nasdaq.com/api/v1/historical/'
HISTORICAL_SUFFIX = '/stocks/2011-03-24/2021-03-24'

DOWNLOAD_FILENAME = '/Users/steve/Downloads/HistoricalQuotes.csv'
HISTORICAL_DIR = '/Users/steve/Desktop/tradeX/data/historical_price/'

START_FROM_SYMBOL = 'PSFF'
RANDOM_SLEEP_LOWER_BOUND = 0
RANDOM_SLEEP_UPPER_BOUND = 5

if __name__ == '__main__':
  with webdriver.Chrome() as driver:
    with open(SYMBOL_FILE, 'r') as csvfile:
      reader = csv.reader(csvfile, delimiter=',')
      next(reader)

      start_parsing = False
      for row in reader:
        symbol = row[0]
        if symbol == START_FROM_SYMBOL:
          start_parsing = True

        if not start_parsing:
          continue

        print(symbol)
        url = HISTORICAL_PREFIX + symbol + HISTORICAL_SUFFIX
        driver.get(url)

        accumulated_time = 0
        while not os.path.exists(DOWNLOAD_FILENAME):
          time.sleep(1)
          accumulated_time += 1
          if accumulated_time > 10:
            break

        if os.path.isfile(DOWNLOAD_FILENAME):
          shutil.copy(DOWNLOAD_FILENAME, HISTORICAL_DIR + symbol + '.csv')
          os.remove(DOWNLOAD_FILENAME)
        else:
          print('file does not exist: ' + symbol)

        time.sleep(random.randint(RANDOM_SLEEP_LOWER_BOUND, RANDOM_SLEEP_UPPER_BOUND))
