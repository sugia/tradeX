'''
This file trains a multi-class classification neural network model
to classify stock price changes based on unions of financial statements.

Experimental result shows that, after 500 epochs:
the accuracy on training set is 0.8102825284004211;
the accuracy on dev set is 0.7362831830978394;

477/477 [==============================] - 2s 4ms/step - loss: 0.5333 - categorical_accuracy: 0.7531
[0.5333253741264343, 0.7530815601348877]
53/53 [==============================] - 0s 5ms/step - loss: 0.5509 - categorical_accuracy: 0.7469
[0.5509482026100159, 0.7469026446342468]
'''
import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow as tf
import os
import random

def aug(X_train, y_train, k=5000):
  X_res, y_res = [], []

  dic = {
    0: [],
    1: [],
    2: [],
    3: [],
    4: [],
  }

  for i in range(len(X_train)):
    if y_train[i][0]:
      dic[0].append((X_train[i], y_train[i]))
    elif y_train[i][1]:
      dic[1].append((X_train[i], y_train[i]))
    elif y_train[i][2]:
      dic[2].append((X_train[i], y_train[i]))
    elif y_train[i][3]:
      dic[3].append((X_train[i], y_train[i]))
    elif y_train[i][4]:
      dic[4].append((X_train[i], y_train[i]))

  res = []
  for i in range(5):
    for _ in range(k):
      res.append(random.choice(dic[i]))

  for row in res:
    a, b = row
    X_res.append(a)
    y_res.append(b)

  return X_res, y_res


if __name__ == '__main__':
  file = '../data/processed_data/combined_filtered_data_union.txt'
  model_path = '../tmp/combined_filtered_data_union_l2_aug.model'

  X = []
  y = []

  with open(file, 'r') as f:
    next(f)
    content = f.read().split('\n')
    for row in content:
      data = row.split(',')
      if len(data) > 4:
        value = float(data[4])
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

        X.append([0.0 if not x else float(x) for x in data[5:]])

  print(len(X))
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)

  X_train, y_train = aug(X_train, y_train)

  model = None
  if os.path.exists(model_path):
    print('~~~~~ reusing existing model')
    model = tf.keras.models.load_model(model_path)
  else:
    print('~~~~~ creating new model')
    input_dim = len(X_train[0])
    model = tf.keras.Sequential([
      tf.keras.layers.InputLayer(input_shape=(input_dim,)),
      tf.keras.layers.LayerNormalization(),
      tf.keras.layers.Dense(
        1024,
        activation='sigmoid',
        kernel_initializer=tf.keras.initializers.GlorotNormal(),
        kernel_regularizer='l2',
      ),
      tf.keras.layers.LayerNormalization(),
      tf.keras.layers.Dense(
        1024,
        activation='sigmoid',
        kernel_initializer=tf.keras.initializers.GlorotNormal(),
        kernel_regularizer='l2',
      ),
      tf.keras.layers.LayerNormalization(),
      tf.keras.layers.Dense(
        5,
        activation='softmax',
        kernel_initializer=tf.keras.initializers.GlorotNormal(),
        kernel_regularizer='l2',
      ),
    ])
    loss_fn = tf.keras.losses.CategoricalCrossentropy()
    model.compile(
      optimizer='adam',
      loss=loss_fn,
      metrics=[tf.keras.metrics.CategoricalAccuracy()]
    )

  model.fit(X_train, y_train, epochs=100, batch_size=32)
  model.save(model_path)

  print(model.evaluate(X_train, y_train))
  print(model.evaluate(X_test, y_test))

