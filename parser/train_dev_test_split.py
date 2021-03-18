import random
from datetime import datetime
import pickle

def dataVarification(X, y):
  dic = {}
  for i in range(len(X)):
    for j in range(len(X[i])):
      key = len(X[i][j])
      if key not in dic:
        dic[key] = 0
      dic[key] += 1

  print(dic)

def getData(file_path):
  symbol_vec_map = {}
  with open(file_path, 'r') as f:
    next(f)
    content = f.read().split('\n')
    for row in content:
      if not row:
        continue

      tokens = row.split(',')
      if tokens[0] not in symbol_vec_map:
        symbol_vec_map[tokens[0]] = []

      try:
        tokens.append(datetime.strptime(tokens[1], '%m/%d/%Y'))
        symbol_vec_map[tokens[0]].append(tokens[1:])
      except:
        pass

  X = []
  y = []
  z = []

  for symbol in symbol_vec_map:
    symbol_vec_map[symbol].sort(key=lambda x: x[-1])
    for i in range(len(symbol_vec_map[symbol]) - 1):
      prev_data = symbol_vec_map[symbol][i][4:-1]
      curr_data = symbol_vec_map[symbol][i+1][4:-1]
      X.append([
        [0.0 if not x else float(x) for x in prev_data],
        [0.0 if not x else float(x) for x in curr_data]
      ])

      value = float(symbol_vec_map[symbol][i+1][3])

      if value >= 200:
        y.append([0,0,0,0,0,0,1])
      elif value >= 150:
        y.append([0,0,0,0,0,1,0])
      elif value >= 100:
        y.append([0,0,0,0,1,0,0])
      elif value >= 50:
        y.append([0,0,0,1,0,0,0])
      elif value >= 0:
        y.append([0,0,1,0,0,0,0])
      elif value >= -50:
        y.append([0,1,0,0,0,0,0])
      else:
        y.append([1,0,0,0,0,0,0])

      z.append([symbol, symbol_vec_map[symbol][i][0], symbol_vec_map[symbol][i+1][0]])

  pre_shuffle_list = list(zip(X, y, z))
  random.shuffle(pre_shuffle_list)
  X, y, z = zip(*pre_shuffle_list)

  return X, y, z

if __name__ == '__main__':
  input_path = '../data/processed_data/combined_filtered_data_union.txt'
  input_path_augmentation = '../data/processed_data/combined_filtered_data_union_augmentation.txt'
  output_train = '../data/processed_data/train.pickle'
  output_dev = '../data/processed_data/dev.pickle'
  output_test = '../data/processed_data/test.pickle'

  org_X, org_y, org_z = getData(input_path)

  dataVarification(org_X, org_y)

  X_dev = org_X[:1000]
  y_dev = org_y[:1000]
  z_dev = org_z[:1000]

  with open(output_dev, 'wb') as f:
    pickle.dump((X_dev, y_dev, z_dev), f)


  X_test = org_X[1000:2000]
  y_test = org_y[1000:2000]
  z_test = org_z[1000:2000]

  with open(output_test, 'wb') as f:
    pickle.dump((X_test, y_test, z_test), f)


  aug_X, aug_y, aug_z = getData(input_path_augmentation)
  dataVarification(aug_X, aug_y)

  X_train = org_X[2000:] + aug_X
  y_train = org_y[2000:] + aug_y
  z_train = org_z[2000:] + aug_z

  with open(output_train, 'wb') as f:
    pickle.dump((X_train, y_train, z_train), f)






