from datetime import datetime
from sklearn.model_selection import train_test_split
import numpy as np
import tensorflow as tf
import os
import copy
import random

def dataView(y):
  res = [0,0,0,0,0]
  for row in y:
    for i in range(len(row)):
      if row[i] == 1:
        res[i] += 1
  print(res)

def dataViewSequence(y):
  res = [0,0,0,0,0]
  for row in y:
    for item in row:
      for i in range(len(item)):
        if item[i] == 1:
          res[i] += 1
  print(res)

def getCategoryLabel(value):
  if value >= 100:
    return [0,0,0,0,1]
  elif value >= 50:
    return [0,0,0,1,0]
  elif value >= 0:
    return [0,0,1,0,0]
  elif value >= -50:
    return [0,1,0,0,0]

  return [1,0,0,0,0]

def getCategoryNum(vec):
  for i in range(len(vec)):
    if vec[i] == 1:
      return i
  return -1

def predictLabelFiltering(y):
  res = [[0 for j in range(len(y[0]))] for i in range(len(y))]
  for i in range(len(y)):
    col = -1
    for j in range(len(y[i])):
      if col == -1 or y[i][col] < y[i][j]:
        col = j
    res[i][col] = 1
  return res

def analysis(x, y, model):
  y_hat = model.predict(x)
  for i in range(len(y_hat)):
    y_hat[i] = predictLabelFiltering(y_hat[i])
    if (y_hat[i][-1] - y[i][-1]).any():
      print(y_hat[i][-1], ' ', y[i][-1])

def prediction(x_test, x_test_label, model):
  res = []
  predicted = model.predict(x_test)
  for i in range(len(predicted)):
    res.append((x_test_label[i], predictLabelFiltering(predicted[i]), getCategoryNum(predictLabelFiltering(predicted[i])[-1])))

  res.sort(key = lambda x: x[-1], reverse=True)
  for row in res:
    print(row)


def train():
  input_path = '../data/processed_data/test.txt'
  model_path = '../tmp/model_simple_lstm512_dense512.model'

  symbol_vec_map = {}
  with open(input_path, 'r') as f:
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

  x_default = []
  y_default = []

  x_test = []
  x_test_label = []

  for symbol in symbol_vec_map:
    symbol_vec_map[symbol].sort(key=lambda x: x[-1])
    for i in range(len(symbol_vec_map[symbol]) - 2):
      curr_data = symbol_vec_map[symbol][i][4:-1]
      next_data = symbol_vec_map[symbol][i+1][4:-1]
      futu_data = symbol_vec_map[symbol][i+2][4:-1]

      if 'None' == symbol_vec_map[symbol][i][3] or 'None' == symbol_vec_map[symbol][i+1][3] or 'None' == symbol_vec_map[symbol][i+2][3]:
        x_test.append([
          [0.0 if not x else float(x) for x in curr_data],
          [0.0 if not x else float(x) for x in next_data],
          [0.0 if not x else float(x) for x in futu_data],
        ])
        x_test_label.append((symbol, symbol_vec_map[symbol][i][0], symbol_vec_map[symbol][i+1][0], symbol_vec_map[symbol][i+2][0]))
      else:
        x_default.append([
          [0.0 if not x else float(x) for x in curr_data],
          [0.0 if not x else float(x) for x in next_data],
          [0.0 if not x else float(x) for x in futu_data],
        ])

        curr_value = float(symbol_vec_map[symbol][i][3])
        next_value = float(symbol_vec_map[symbol][i+1][3])
        futu_value = float(symbol_vec_map[symbol][i+2][3])
        y_default.append([
          getCategoryLabel(curr_value),
          getCategoryLabel(next_value),
          getCategoryLabel(futu_value),
        ])

  x_train, x_dev, y_train, y_dev = train_test_split(x_default, y_default, test_size=0.1)
  print(len(x_train), len(y_train), len(x_dev), len(y_dev))

  dataViewSequence(y_train)
  dataViewSequence(y_dev)

  model = None
  if os.path.exists(model_path):
    print('~~~~~ reuses existing model')
    model = tf.keras.models.load_model(model_path)
  else:
    print('~~~~~ creates new model')
    input_dim_first = len(x_train[0])
    input_dim_second = len(x_train[0][0])
    model = tf.keras.Sequential([
      tf.keras.layers.InputLayer(input_shape=(input_dim_first, input_dim_second)),
      tf.keras.layers.LSTM(
        512,
        activation=tf.keras.activations.tanh,
        return_sequences=True,
      ),
      tf.keras.layers.Dropout(rate=0.1),
      tf.keras.layers.Dense(
        512,
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

  '''
  print('~~~~~ start model fit')
  model.summary()
  model.fit(x_train, y_train, epochs=100, batch_size=32)
  model.save(model_path)
  '''

  print(model.evaluate(x_train, y_train))
  print(model.evaluate(x_dev, y_dev))

  # analysis(x_train, y_train, model)

  prediction(x_test, x_test_label, model)

if __name__ == '__main__':
  while True:
    train()
