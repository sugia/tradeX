'''
income statement, balance sheet, cash flow statement
This file uses selenium chromedriver to parse financial statements from nasdaq.com
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
FINANCIAL_STATEMENT_PREFIX = 'http://nasdaq.com/market-activity/stocks/'
FINANCIAL_STATEMENT_SUFFIX = '/financials'

INCOME_STATEMENT_DIR = '../data/income_statement/'
BALANCE_SHEET_DIR = '../data/balance_sheet/'
CASH_FLOW_DIR = '../data/cash_flow_statement/'

RANDOM_SLEEP_LOWER_BOUND = 2
RANDOM_SLEEP_UPPER_BOUND = 4

if __name__ == '__main__':
  with webdriver.Chrome() as driver:
    wait = WebDriverWait(driver, 10)
    with open(SYMBOL_FILE, 'r') as csvfile:
      reader = csv.reader(csvfile, delimiter=',')
      next(reader)

      for row in reader:
        symbol = row[0]

        url = FINANCIAL_STATEMENT_PREFIX + symbol + FINANCIAL_STATEMENT_SUFFIX
        driver.get(url)
        time.sleep(random.randint(RANDOM_SLEEP_LOWER_BOUND, RANDOM_SLEEP_UPPER_BOUND))

        # income statement
        try:
          content = wait.until(presence_of_element_located((By.CLASS_NAME, 'financials__table')))
          print('~~~~~~~~~~ {} income statement ~~~~~~~~~~'.format(symbol))
          print(content.text)

          with open(INCOME_STATEMENT_DIR + symbol + '.txt', 'w') as wfile:
            wfile.write(content.text)
        except:
          pass

        # balance sheet
        try:
          driver.find_element_by_xpath('//button[contains(text(), "Balance Sheet")]').click()
          time.sleep(random.randint(RANDOM_SLEEP_LOWER_BOUND, RANDOM_SLEEP_UPPER_BOUND))
        except:
          pass

        try:
          element = driver.find_elements_by_class_name('financials__table')
          content = element[1]
          print('~~~~~~~~~~ {} balance sheet ~~~~~~~~~~'.format(symbol))
          print(content.text)

          with open(BALANCE_SHEET_DIR + symbol + '.txt', 'w') as wfile:
            wfile.write(content.text)
        except:
          pass

        # cash flow statement
        try:
          driver.find_element_by_xpath('//button[contains(text(), "Cash Flow")]').click()
          time.sleep(random.randint(RANDOM_SLEEP_LOWER_BOUND, RANDOM_SLEEP_UPPER_BOUND))
        except:
          pass

        try:
          element = driver.find_elements_by_class_name('financials__table')
          content = element[2]
          print('~~~~~~~~~~ {} cash flow statement ~~~~~~~~~~'.format(symbol))
          print(content.text)

          with open(CASH_FLOW_DIR + symbol + '.txt', 'w') as wfile:
            wfile.write(content.text)
        except:
          pass


