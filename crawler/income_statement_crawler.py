'''
This file uses selenium chromedriver to parse income statements from nasdaq.com
Data is stored in ../data/income_statement/.

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
INCOME_STATEMENT_PREFIX = 'http://nasdaq.com/market-activity/stocks/'
INCOME_STATEMENT_SUFFIX = '/financials'

INCOME_STATEMENT_DIR = '../data/income_statement/'

RANDOM_SLEEP_LOWER_BOUND = 2
RANDOM_SLEEP_UPPER_BOUND = 5

if __name__ == '__main__':
  with webdriver.Chrome() as driver:
    wait = WebDriverWait(driver, 10)
    with open(SYMBOL_FILE, 'r') as csvfile:
      reader = csv.reader(csvfile, delimiter=',')
      next(reader)

      start_parsing = False
      for row in reader:
        symbol = row[0]

        url = INCOME_STATEMENT_PREFIX + symbol + INCOME_STATEMENT_SUFFIX
        driver.get(url)
        time.sleep(random.randint(RANDOM_SLEEP_LOWER_BOUND, RANDOM_SLEEP_UPPER_BOUND))
        try:
          content = wait.until(presence_of_element_located((By.CLASS_NAME, 'financials__table')))
          print('~~~~~~~~~~ {} ~~~~~~~~~~'.format(symbol))
          print(content.text)

          with open(INCOME_STATEMENT_DIR + symbol + '.txt', 'w') as wfile:
            wfile.write(content.text)
        except:
          pass

