'''
This file uses selenium chromedriver to parse balance sheets from nasdaq.com.
Data is stored in ../data/balance_sheet/.

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
BALANCE_SHEET_PREFIX = 'http://nasdaq.com/market-activity/stocks/'
BALANCE_SHEET_SUFFIX = '/financials'

BALANCE_SHEET_DIR = '../data/balance_sheet/'

RANDOM_SLEEP_LOWER_BOUND = 1
RANDOM_SLEEP_UPPER_BOUND = 4

if __name__ == '__main__':
  with webdriver.Chrome() as driver:
    driver.set_page_load_timeout(3)
    wait = WebDriverWait(driver, 1)
    with open(SYMBOL_FILE, 'r') as csvfile:
      reader = csv.reader(csvfile, delimiter=',')
      next(reader)

      start_parsing = False
      for row in reader:
        symbol = row[0]

        url = BALANCE_SHEET_PREFIX + symbol + BALANCE_SHEET_SUFFIX
        try:
          driver.get(url)
        except:
          pass

        time.sleep(random.randint(RANDOM_SLEEP_LOWER_BOUND, RANDOM_SLEEP_UPPER_BOUND))

        try:
          driver.find_element_by_xpath('//button[contains(text(), "Balance Sheet")]').click()
        except:
          pass

        time.sleep(random.randint(RANDOM_SLEEP_LOWER_BOUND, RANDOM_SLEEP_UPPER_BOUND))

        try:
          element = driver.find_elements_by_class_name('financials__table')
          content = element[1]
          print('~~~~~~~~~~ {} ~~~~~~~~~~'.format(symbol))
          print(content.text)

          with open(BALANCE_SHEET_DIR + symbol + '.txt', 'w') as wfile:
            wfile.write(content.text)
        except:
          pass

