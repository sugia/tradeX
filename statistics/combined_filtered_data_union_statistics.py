'''
This file processes income statement filtered data and generates key value pairs,
with percentage change as key, and the number of stocks as value.
'''
import numpy as np


if __name__ == '__main__':
  file = '../data/processed_data/combined_filtered_data_union.txt'
  vec = []
  with open(file, 'r') as f:
    next(f)
    content = f.read().split('\n')
    for row in content:
      data = row.split(',')
      if len(data) > 4:
        value = float(data[4])
        vec.append((data[0], data[1], value))


  vec.sort(key = lambda x: x[2])

  for row in vec:
    print('\t'.join(row))

