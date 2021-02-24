from datetime import datetime
from sklearn.model_selection import train_test_split
import numpy as np
import tensorflow as tf
import os

if __name__ == '__main__':
  input_path = '../data/processed_data/combined_filtered_data_union.txt'
  model_path = '../tmp/combined_filtered_data_union_neural_lstm.model'

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
    for i in range(len(symbol_vec_map[symbol]) - 1):
      prev_data = symbol_vec_map[symbol][i][4:-1]
      curr_data = symbol_vec_map[symbol][i+1][4:-1]
      X.append([
        [0.0 if not x else float(x) for x in prev_data],
        [0.0 if not x else float(x) for x in curr_data]
      ])

      value = float(symbol_vec_map[symbol][i+1][3])

      if value >= 100:
        y.append([0,0,0,0,0,1])
      elif value >= 50:
        y.append([0,0,0,0,1,0])
      elif value >= 0:
        y.append([0,0,0,1,0,0])
      elif value >= -50:
        y.append([0,0,1,0,0,0])
      elif value >= -100:
        y.append([0,1,0,0,0,0])
      else:
        y.append([1,0,0,0,0,0])

  print(np.array(X).shape)
  print(np.array(y).shape)
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

  model = None
  if os.path.exists(model_path):
    print('~~~~~ reusing existing model')
    model = tf.keras.models.load_model(model_path)
  else:
    print('~~~~~ creating new model')
    input_dim_first = len(X_train[0])
    input_dim_second = len(X_train[0][0])

    print(input_dim_first, input_dim_second)
    model = tf.keras.Sequential([
      tf.keras.layers.InputLayer(input_shape=(input_dim_first, input_dim_second)),
      tf.keras.layers.LSTM(
        1024,
        activation='softmax',
        kernel_initializer=tf.keras.initializers.GlorotNormal(),
        # kernel_regularizer='l2',
      ),
      tf.keras.layers.Dense(
        1024,
        activation='softmax',
        kernel_initializer=tf.keras.initializers.GlorotNormal(),
        # kernel_regularizer='l2',
      ),
      tf.keras.layers.Dense(
        6,
        activation='softmax',
        kernel_initializer=tf.keras.initializers.GlorotNormal(),
        # kernel_regularizer='l2',
      ),
    ])
    loss_fn = tf.keras.losses.CategoricalCrossentropy()
    model.compile(
      optimizer='adam',
      loss=loss_fn,
      metrics=[tf.keras.metrics.CategoricalAccuracy()]
    )

  print('~~~~~ start model fit')
  model.fit(X_train, y_train, epochs=500, batch_size=32)
  model.save(model_path)

  print(model.evaluate(X_train, y_train))
  print(model.evaluate(X_test, y_test))
  '''
  500 epochs
  train 0.7515571117401123
  dev 0.7682878375053406
  '''

