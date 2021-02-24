'''
This file uses selenium chromedriver to parse cash flow statements from nasdaq.com
Data is stored in ../data/cash_flow_statement/.

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
CASH_FLOW_PREFIX = 'http://nasdaq.com/market-activity/stocks/'
CASH_FLOW_SUFFIX = '/financials'

CASH_FLOW_DIR = '../data/cash_flow_statement/'

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

        url = CASH_FLOW_PREFIX + symbol + CASH_FLOW_SUFFIX
        try:
          driver.get(url)
        except:
          pass

        time.sleep(random.randint(RANDOM_SLEEP_LOWER_BOUND, RANDOM_SLEEP_UPPER_BOUND))

        try:
          driver.find_element_by_xpath('//button[contains(text(), "Cash Flow")]').click()
        except:
          pass

        time.sleep(random.randint(RANDOM_SLEEP_LOWER_BOUND, RANDOM_SLEEP_UPPER_BOUND))

        try:
          element = driver.find_elements_by_class_name('financials__table')
          content = element[2]
          print('~~~~~~~~~~ {} ~~~~~~~~~~'.format(symbol))
          print(content.text)

          with open(CASH_FLOW_DIR + symbol + '.txt', 'w') as wfile:
            wfile.write(content.text)
        except:
          pass

