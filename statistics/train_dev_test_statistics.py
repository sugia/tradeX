'''
train
0 3121
1 15207
2 58113
3 7749
4 2572
5 1105
6 1789

dev
0 36
1 168
2 743
3 28
4 8
5 6
6 11

test
0 41
1 188
2 715
3 37
4 7
5 2
6 10
'''
from datetime import datetime
from sklearn.model_selection import train_test_split
import numpy as np
import tensorflow as tf
import os
import pickle

def getKey(y):
  assert sum(y) == 1
  for i in range(len(y)):
    if y[i] == 1:
      return i

def showStatistics(y):
  dic = {}

  for i in range(len(y)):
    key = getKey(y[i])
    if key not in dic:
      dic[key] = 0

    dic[key] += 1

  for key in sorted(dic.keys()):
    print(key, dic[key])

if __name__ == '__main__':
  train_file = '../data/processed_data/train.pickle'
  dev_file = '../data/processed_data/dev.pickle'
  test_file = '../data/processed_data/test.pickle'

  with open(train_file, 'rb') as f:
    X_train, y_train, z_train = pickle.load(f)
  print('train')
  showStatistics(y_train)

  with open(dev_file, 'rb') as f:
    X_dev, y_dev, z_dev = pickle.load(f)
  print('dev')
  showStatistics(y_dev)

  with open(test_file, 'rb') as f:
    X_test, y_test, z_test = pickle.load(f)
  print('test')
  showStatistics(y_test)
