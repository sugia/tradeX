'''
This file processes cash flow statement filtered data and generates key value pairs,
with percentage change as key, and the number of stocks as value.
'''
import numpy as np

if __name__ == '__main__':
  file = '../data/processed_data/cash_flow_statement_filtered_data.txt'
  dic = {}
  with open(file, 'r') as f:
    next(f)
    content = f.read().split('\n')
    for row in content:
      data = row.split(',')
      if len(data) > 4:
        value = float(data[4])
        key = int(value)
        if key not in dic:
          dic[key] = 0
        dic[key] += 1


  for k in sorted(dic.keys()):
    print('{}\t{}'.format(k, dic[k]))