'''
This file combines data from balance sheet, income statement, cash flow statement
to get unions, and stores those unions into
../data/processed_data/combined_filtered_data_union.txt
'''

import random

def getMapAndHeaderFromFile(file_path):
  # key: (Symbol,Period Ending), value: list of the rest
  res = {}
  res_header = []
  with open(file_path, 'r') as f:
    content = f.read().split('\n')
    res_header = content[0].split(',')
    content.pop(0)
    for row in content:
      tokens = row.split(',')
      key = tokens[:2]
      value = tokens[2:]

      if tuple(key) not in res:
        res[tuple(key)] = []

      res[tuple(key)].append(value)

  return res, res_header

if __name__ == '__main__':
  balance_sheet_filtered_data_path = '../data/processed_data/balance_sheet_filtered_data_augmentation.txt'
  income_statement_filtered_data_path = '../data/processed_data/income_statement_filtered_data_augmentation.txt'
  cash_flow_statement_filtered_data_path = '../data/processed_data/cash_flow_statement_filtered_data_augmentation.txt'


  balance_sheet, balance_sheet_header = getMapAndHeaderFromFile(balance_sheet_filtered_data_path)
  print(len(balance_sheet))
  print(balance_sheet_header)
  print(len(balance_sheet_header)) # 35
  tmp_balance_sheet = {}
  for k in balance_sheet:
    v = len(balance_sheet[k])
    if v not in tmp_balance_sheet:
      tmp_balance_sheet[v] = 0
    tmp_balance_sheet[v] += 1
  print(tmp_balance_sheet)

  income_statement, income_statement_header = getMapAndHeaderFromFile(income_statement_filtered_data_path)
  print(len(income_statement))
  print(income_statement_header)
  print(len(income_statement_header)) # 24
  tmp_income_statement = {}
  for k in income_statement:
    v = len(income_statement[k])
    if v not in tmp_income_statement:
      tmp_income_statement[v] = 0
    tmp_income_statement[v] += 1
  print(tmp_income_statement)

  cash_flow_statement, cash_flow_statement_header = getMapAndHeaderFromFile(cash_flow_statement_filtered_data_path)
  print(len(cash_flow_statement))
  print(cash_flow_statement_header)
  print(len(cash_flow_statement_header)) # 23
  tmp_cash_flow_statement = {}
  for k in cash_flow_statement:
    v = len(cash_flow_statement[k])
    if v not in tmp_cash_flow_statement:
      tmp_cash_flow_statement[v] = 0
    tmp_cash_flow_statement[v] += 1
  print(tmp_cash_flow_statement)

  key_set = set()
  for k in balance_sheet:
    key_set.add(k)
  for k in income_statement:
    key_set.add(k)
  for k in cash_flow_statement:
    key_set.add(k)

  tmp_dic = {}
  output_path = '../data/processed_data/combined_filtered_data_union_augmentation.txt'
  with open(output_path, 'w') as f:
    f.write(','.join(balance_sheet_header) + ',' +
      ','.join(income_statement_header[2:]) + ',' +
      ','.join(cash_flow_statement_header[2:]) +
      '\n')
    for k in key_set:
      if k not in balance_sheet:
        balance_sheet[k] = [['0'] * (len(balance_sheet_header) - 2)]
      if k not in income_statement:
        income_statement[k] = [['0'] * (len(income_statement_header) - 2)]
      if k not in cash_flow_statement:
        cash_flow_statement[k] = [['0'] * (len(cash_flow_statement_header) - 2)]

      l = len(balance_sheet[k][0]) + len(income_statement[k][0]) + len(cash_flow_statement[k][0])
      if l in tmp_dic:
        tmp_dic[l] += 1
      else:
        tmp_dic[l] = 1

      for _ in range(5):
        '''
        print(len(random.choice(balance_sheet[k])))
        print(len(random.choice(income_statement[k])))
        print(len(random.choice(cash_flow_statement[k])))
        '''
        bbb = random.choice(balance_sheet[k])
        iii = random.choice(income_statement[k])
        ccc = random.choice(cash_flow_statement[k])
        if len(bbb) + len(iii) + len(ccc) != 75:
          continue
        f.write(','.join(k) + ',' +
          ','.join(random.choice(balance_sheet[k])) + ',' +
          ','.join(random.choice(income_statement[k])) + ',' +
          ','.join(random.choice(cash_flow_statement[k])) +
          '\n')

  print(tmp_dic)
