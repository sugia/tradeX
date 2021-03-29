import os
import datetime

def getNextPeriodStart(period_ending):
  period_ending_date = datetime.datetime.strptime(period_ending, '%m/%d/%Y')
  next_period_start_date = period_ending_date + datetime.timedelta(days=1)
  return next_period_start_date

def getNextPeriodEnd(period_ending):
  period_ending_date = datetime.datetime.strptime(period_ending, '%m/%d/%Y')
  next_period_end_date = period_ending_date + datetime.timedelta(days=365)
  return next_period_end_date

def getHistoricalLabels(symbol, period_ending):
  historical_directory = '../data/historical_price/'
  next_period_start = getNextPeriodStart(period_ending)
  next_period_end = getNextPeriodEnd(period_ending)

  next_period_start_opening_price = None
  next_period_end_closing_price = None

  top_date = None
  with open(historical_directory + symbol + '.csv', 'r') as f:
    next(f)
    content = f.read().split('\n')
    for line in content:
      if not line:
        continue

      vec = line.split(', ')
      current_date = datetime.datetime.strptime(vec[0], '%m/%d/%Y')
      if not top_date:
        top_date = current_date
        if top_date < next_period_end:
          if next_period_start_opening_price == None:
            next_period_start_opening_price = 'None'
          if next_period_end_closing_price == None:
            next_period_end_closing_price = 'None'
          return [
            next_period_start_opening_price,
            next_period_end_closing_price,
            'None'
          ]

      if current_date >= next_period_start:
        next_period_start_opening_price = vec[3].replace('$', '').replace(',', '')
      else:
        break
      if current_date >= next_period_end:
        next_period_end_closing_price = vec[1].replace('$', '').replace(',', '')

  if next_period_start_opening_price == None or next_period_end_closing_price == None:
    if next_period_start_opening_price == None:
      next_period_start_opening_price = 'None'
    if next_period_end_closing_price == None:
      next_period_end_closing_price = 'None'
    return [
      next_period_start_opening_price,
      next_period_end_closing_price,
      'None'
    ]
  return [
    next_period_start_opening_price,
    next_period_end_closing_price,
    str(100 * (float(next_period_end_closing_price) - float(next_period_start_opening_price)) / float(next_period_start_opening_price))
  ]

def readFeatures(read_directory, dic, statement_type):
  print(read_directory)
  read_files = os.listdir(read_directory)
  for file in read_files:
    file_path = read_directory + file
    symbol = file.replace('.txt', '').strip()
    # print(symbol)
    if not os.path.exists('../data/historical_price/' + symbol + '.csv'):
      # print('~~~~~ error: historical file does not exist: ' + symbol)
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

      if (symbol, a[0]) not in dic:
        dic[(symbol, a[0])] = {}
      dic[(symbol, a[0])][statement_type] = a[1:]

      if (symbol, b[0]) not in dic:
        dic[(symbol, b[0])] = {}
      dic[(symbol, b[0])][statement_type] = b[1:]

      if (symbol, c[0]) not in dic:
        dic[(symbol, c[0])] = {}
      dic[(symbol, c[0])][statement_type] = c[1:]

      if (symbol, d[0]) not in dic:
        dic[(symbol, d[0])] = {}
      dic[(symbol, d[0])][statement_type] = d[1:]

if __name__ == '__main__':
  balance_sheet_directory = '../data/balance_sheet/'
  income_statement_directory = '../data/income_statement/'
  cash_flow_statement_directory = '../data/cash_flow_statement/'
  write_directory = '../data/processed_data/'

  # (symbol, datetime): {[b, i, c][features]}
  dic = {}
  readFeatures(balance_sheet_directory, dic, 'b')
  readFeatures(income_statement_directory, dic, 'i')
  readFeatures(cash_flow_statement_directory, dic, 'c')

  print(len(dic))
  for k in sorted(list(set(dic.keys()))):
    if 'b' in dic[k] and 'i' in dic[k] and 'c' in dic[k]:
      row = list(k) + getHistoricalLabels(k[0], k[1])
      for s in ['b', 'i', 'c']:
        row += dic[k][s]

      with open(write_directory + 'test.txt', 'a') as out_file:
        out_file.write(','.join(row) + '\n')

    else:
      # print(k)
      pass







