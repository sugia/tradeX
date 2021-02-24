'''
This file trains a binary classification neural network model
to classify up/down of stock price based on onlly income statement.
The goal is to see if it is learnable to predict stock performance
based on only income statement.

Experimental result shows that, after 500 epochs:
the accuracy on training set is 0.5794054269790649;
the accuracy on dev set is 0.5820801854133606;
'''
import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow as tf
import os

if __name__ == '__main__':
  file = '../data/processed_data/income_statement_filtered_data.txt'
  model_path = '../tmp/income_statement_filtered_data_neural.model'

  X = []
  y = []
  pos = 0
  neg = 0
  with open(file, 'r') as f:
    next(f)
    content = f.read().split('\n')
    for row in content:
      data = row.split(',')
      if len(data) > 4:
        if float(data[4]) > 0:
          y.append(True)
          pos += 1
        else:
          y.append(False)
          neg += 1
        X.append([0.0 if not x else float(x) for x in data[5:]])

  print(pos, neg, 1.0 * max(pos, neg) / (pos + neg))

  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)

  model = None
  if os.path.exists(model_path):
    model = tf.keras.models.load_model(model_path)
  else:
    input_dim = len(X_train[0])
    model = tf.keras.Sequential([
      tf.keras.layers.InputLayer(input_shape=(input_dim,)),
      tf.keras.layers.Dense(
        1024,
        activation='sigmoid',
        kernel_initializer=tf.keras.initializers.GlorotNormal(),
        # kernel_regularizer='l2',
      ),
      tf.keras.layers.Dense(
        1024,
        activation='sigmoid',
        kernel_initializer=tf.keras.initializers.GlorotNormal(),
        # kernel_regularizer='l2',
      ),
      tf.keras.layers.Dense(
        1,
        activation='sigmoid',
        kernel_initializer=tf.keras.initializers.GlorotNormal(),
        # kernel_regularizer='l2',
      ),
    ])
    loss_fn = tf.keras.losses.BinaryCrossentropy()
    model.compile(
      optimizer='adam',
      loss=loss_fn,
      metrics=[tf.keras.metrics.BinaryAccuracy()]
    )

  model.fit(X_train, y_train, epochs=500, batch_size=32)
  model.save(model_path)

  print(model.evaluate(X_train, y_train))
  print(model.evaluate(X_test, y_test))
