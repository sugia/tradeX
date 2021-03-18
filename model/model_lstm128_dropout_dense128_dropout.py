'''
This file trains a multi-class classification neural network model with LSTM
to classify stock price changes based on unions of financial statements.

'''
from datetime import datetime
from sklearn.model_selection import train_test_split
import numpy as np
import tensorflow as tf
import os
import copy
import random

def aug(X_train, y_train):
  X_res, y_res = [], []

  for i in range(len(X_train)):
    X_res.append(copy.deepcopy(X_train[i]))
    y_res.append(copy.deepcopy(y_train[i]))

    for _ in range(4):
      X_res.append(copy.deepcopy(X_train[i]))
      y_res.append(copy.deepcopy(y_train[i]))

      for row_idx in range(len(X_res[-1])):
        for col_idx in range(len(X_res[-1][row_idx])):
          X_res[-1][row_idx][col_idx] += X_res[-1][row_idx][col_idx] * 0.01 * random.randint(-5, 5)

    # removes balance sheet 30
    X_res.append(copy.deepcopy(X_train[i]))
    y_res.append(copy.deepcopy(y_train[i]))
    for row_idx in range(len(X_res[-1])):
      for col_idx in range(30):
        X_res[-1][row_idx][col_idx] = 0.0

    # removes income statement 30 + 21
    X_res.append(copy.deepcopy(X_train[i]))
    y_res.append(copy.deepcopy(y_train[i]))
    for row_idx in range(len(X_res[-1])):
      for col_idx in range(30, 30 + 21):
        X_res[-1][row_idx][col_idx] = 0.0

    # removes cash flow statement 30 + 21 + 21
    X_res.append(copy.deepcopy(X_train[i]))
    y_res.append(copy.deepcopy(y_train[i]))
    for row_idx in range(len(X_res[-1])):
      for col_idx in range(30 + 21, 30 + 21 + 21):
        X_res[-1][row_idx][col_idx] = 0.0
  return X_res, y_res


def dataFilter(X, y):
  print('~~~~~~~ dataFilter')
  X_res, y_res = [], []
  total = 0
  count = 0
  idx = 0
  for item in X:
    idx += 1
    for row in item:
      total += 1
      tmp = 0
      for c in row:
        if abs(c) < 1.0:
          tmp += 1
      if tmp * 2 >= len(row):
        count += 1
      else:
        X_res.append(X[idx-1])
        y_res.append(y[idx-1])

  print(count, total)
  return X_res, y_res

def dataView(y):
  res = [0,0,0,0,0]
  for row in y:
    for i in range(len(row)):
      if row[i] == 1:
        res[i] += 1
  print(res)

def train():
  input_path = '../data/processed_data/combined_filtered_data_union.txt'
  model_path = '../tmp/model_lstm128_dropout_dense128_dropout.model'

  symbol_vec_map = {}
  with open(input_path, 'r') as f:
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

  for symbol in symbol_vec_map:
    symbol_vec_map[symbol].sort(key=lambda x: x[-1])
    for i in range(len(symbol_vec_map[symbol]) - 3):
      prev_data = symbol_vec_map[symbol][i][4:-1]
      curr_data = symbol_vec_map[symbol][i+1][4:-1]
      next_data = symbol_vec_map[symbol][i+2][4:-1]
      futu_data = symbol_vec_map[symbol][i+3][4:-1]
      X.append([
        [0.0 if not x else float(x) for x in prev_data],
        [0.0 if not x else float(x) for x in curr_data],
        [0.0 if not x else float(x) for x in next_data],
        [0.0 if not x else float(x) for x in futu_data],
      ])

      value = float(symbol_vec_map[symbol][i+1][3])

      if value >= 100:
        y.append([0,0,0,0,1])
      elif value >= 50:
        y.append([0,0,0,1,0])
      elif value >= 0:
        y.append([0,0,1,0,0])
      elif value >= -50:
        y.append([0,1,0,0,0])
      else:
        y.append([1,0,0,0,0])

  print(np.array(X).shape)
  print(np.array(y).shape)
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)
  print(len(X_train), len(y_train), len(X_test), len(y_test))

  X_train, y_train = aug(X_train, y_train)
  X_train, y_train = dataFilter(X_train, y_train)
  dataView(y_train)

  X_test, y_test = dataFilter(X_test, y_test)
  dataView(y_test)

  print(len(X_train), len(y_train), len(X_test), len(y_test))


  model = None
  if os.path.exists(model_path):
    print('~~~~~ reuses existing model')
    model = tf.keras.models.load_model(model_path)
  else:
    print('~~~~~ creates new model')
    print(len(X_train))
    input_dim_first = len(X_train[0])
    input_dim_second = len(X_train[0][0])

    print(input_dim_first, input_dim_second)
    model = tf.keras.Sequential([
      tf.keras.layers.InputLayer(input_shape=(input_dim_first, input_dim_second)),
      tf.keras.layers.LSTM(
        128,
        activation=tf.keras.activations.tanh,
        # return_sequences=True,
      ),
      tf.keras.layers.Dropout(rate=0.1),
      tf.keras.layers.Dense(
        128,
        activation=tf.keras.activations.tanh,
      ),
      tf.keras.layers.Dropout(rate=0.1),
      tf.keras.layers.Dense(
        5,
        activation=tf.keras.activations.softmax,
      ),
    ])

    loss_fn = tf.keras.losses.CategoricalCrossentropy()
    model.compile(
      optimizer='adam',
      loss=loss_fn,
      metrics=[tf.keras.metrics.CategoricalAccuracy()]
    )

  print('~~~~~ start model fit')
  model.summary()
  model.fit(X_train, y_train, epochs=50, batch_size=32)
  model.save(model_path)

  print(model.evaluate(X_train, y_train))
  print(model.evaluate(X_test, y_test))


if __name__ == '__main__':
  while True:
    train()
