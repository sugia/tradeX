'''
This file parses balance sheet data from ../data/balance_sheet/,
combines with historical price data from ../data/historical_price/,
and stores processed data in ../data/processed_data/balance_sheet_filtered_data_augmentation.txt.
Data augmentation: generates five data points for one year by randomly sampling buying and selling prices
within a month after period ending of balance sheet.
'''
import os
import datetime
import random

def getNextPeriodStart(period_ending, random_date=0):
  period_ending_date = datetime.datetime.strptime(period_ending, '%m/%d/%Y')
  next_period_start_date = period_ending_date + datetime.timedelta(days=1 + random_date)
  return next_period_start_date

def getNextPeriodEnd(period_ending, random_date=0):
  period_ending_date = datetime.datetime.strptime(period_ending, '%m/%d/%Y')
  next_year = period_ending_date.year + 1
  next_period_end_date = period_ending_date
  next_period_end_date = next_period_end_date.replace(year=next_year)
  next_period_end_date = next_period_end_date + datetime.timedelta(days=random_date)
  return next_period_end_date

def getHistoricalLabels(symbol, period_ending, random_date_start=0, random_date_end=0):
  historical_directory = '../data/historical_price/'
  next_period_start = getNextPeriodStart(period_ending, random_date_start)
  next_period_end = getNextPeriodEnd(period_ending, random_date_end)

  next_period_start_opening_price = None
  next_period_end_closing_price = None
  with open(historical_directory + symbol + '.csv', 'r') as f:
    next(f)
    content = f.read().split('\n')
    for line in content:
      if not line:
        continue

      vec = line.split(', ')
      current_date = datetime.datetime.strptime(vec[0], '%m/%d/%Y')
      if current_date >= next_period_start:
        next_period_start_opening_price = vec[3].replace('$', '').replace(',', '')
      if current_date >= next_period_end:
        next_period_end_closing_price = vec[1].replace('$', '').replace(',', '')

  return [
    'Next Period Start Opening Price (Period Ending + 1 Day)',
    'Next Period End Closing Price (Period Ending + 1 year)',
    'Price Percentage Change',
  ], [
    next_period_start_opening_price,
    next_period_end_closing_price,
    str(100 * (float(next_period_end_closing_price) - float(next_period_start_opening_price)) / float(next_period_start_opening_price))
  ]

if __name__ == '__main__':
  read_directory = '../data/balance_sheet/'
  write_directory = '../data/processed_data/'
  write_file_name = 'balance_sheet_filtered_data_augmentation.txt'

  read_files = os.listdir(read_directory)
  is_first_file = True
  for file in read_files:
    file_path = read_directory + file
    symbol = file.replace('.txt', '')
    print(symbol)
    if not os.path.exists('../data/historical_price/' + symbol + '.csv'):
      print('~~~~~ error: historical file does not exist: ' + symbol)
      continue
    with open(file_path, 'r') as f:
      content = f.read().split('\n')
      if not content or len(content) < 5:
        continue

      label = []
      a = []
      b = []
      c = []
      d = []
      for line in content:
        if not line:
          continue
        if len(line.split(' ')) >= 5:
          tmp = line.rsplit(' ', 1)
          d.append(tmp[1].replace('$', '').replace(',', ''))

          tmp = tmp[0].rsplit(' ', 1)
          c.append(tmp[1].replace('$', '').replace(',', ''))

          tmp = tmp[0].rsplit(' ', 1)
          b.append(tmp[1].replace('$', '').replace(',', ''))

          tmp = tmp[0].rsplit(' ', 1)
          a.append(tmp[1].replace('$', '').replace(',', ''))

          label.append(tmp[0].replace(':', ''))

      with open(write_directory + write_file_name, 'a') as wf:
        if is_first_file:
          wf.write(','.join(['Symbol'] + [label[0]] + getHistoricalLabels(symbol, a[0])[0] + label[1:]) + '\n')
          is_first_file = False

        for k in range(5):
          random_date_start = k+1
          random_date_end = random_date_start
          try:
            wf.write(','.join([symbol] + [a[0]] + getHistoricalLabels(symbol, a[0], random_date_start, random_date_end)[1] + a[1:]) + '\n')
          except:
            print('~~~~~ error: {} {}'.format(symbol, a[0]))
          try:
            wf.write(','.join([symbol] + [b[0]] + getHistoricalLabels(symbol, b[0], random_date_start, random_date_end)[1] + b[1:]) + '\n')
          except:
            print('~~~~~ error: {} {}'.format(symbol, b[0]))
          try:
            wf.write(','.join([symbol] + [c[0]] + getHistoricalLabels(symbol, c[0], random_date_start, random_date_end)[1] + c[1:]) + '\n')
          except:
            print('~~~~~ error: {} {}'.format(symbol, c[0]))
          try:
            wf.write(','.join([symbol] + [d[0]] + getHistoricalLabels(symbol, d[0], random_date_start, random_date_end)[1] + d[1:]) + '\n')
          except:
            print('~~~~~ error: {} {}'.format(symbol, d[0]))


