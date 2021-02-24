import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow as tf
import os

if __name__ == '__main__':
  file = '../data/processed_data/combined_filtered_data_union.txt'
  model_path = '../tmp/combined_filtered_data_union_neural.model'

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

        X.append([0.0 if not x else float(x) for x in data[5:]])

  print(len(X))
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

  model = None
  if os.path.exists(model_path):
    print('~~~~~ reusing existing model')
    model = tf.keras.models.load_model(model_path)
  else:
    print('~~~~~ creating new model')
    input_dim = len(X_train[0])
    model = tf.keras.Sequential([
      tf.keras.layers.InputLayer(input_shape=(input_dim,)),
      tf.keras.layers.Dense(
        1024,
        activation='sigmoid',
        kernel_initializer=tf.keras.initializers.GlorotNormal(),
        kernel_regularizer='l2',
      ),
      tf.keras.layers.Dense(
        1024,
        activation='sigmoid',
        kernel_initializer=tf.keras.initializers.GlorotNormal(),
        kernel_regularizer='l2',
      ),
      tf.keras.layers.Dense(
        6,
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

  model.fit(X_train, y_train, epochs=500, batch_size=32)
  model.save(model_path)

  print(model.evaluate(X_train, y_train))
  print(model.evaluate(X_test, y_test))
  '''
  multi classes classification
  500 epochs
  train 0.8102825284004211
  dev 0.7362831830978394
  '''
