'''
This file trains a multi-class classification neural network model with LSTM
to classify stock price changes based on unions of financial statements.

Experimental result shows that, after 500 epochs:
the accuracy on training set is 0.7515571117401123;
the accuracy on dev set is 0.7682878375053406;

[1.9459283351898193, 0.1428571492433548]
[1.9409123659133911, 0.7170000076293945]


'''
from datetime import datetime
from sklearn.model_selection import train_test_split
import numpy as np
import tensorflow as tf
import os
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

def getKey(y):
  assert sum(y) == 1
  for i in range(len(y)):
    if y[i] == 1:
      return i
  raise 'error: unknown y: {}'.format(y)

def getSample(X, y, z, num=1000):
  assert len(X) == len(y)
  assert len(y) == len(z)

  dic = {}
  for i in range(len(X)):
    key = getKey(y[i])
    if key not in dic:
      dic[key] = []

    dic[key].append([X[i], y[i], z[i]])

  sample_X = []
  sample_y = []
  sample_z = []

  for key in dic:
    indexes = [i for i in range(len(dic[key]))]
    sample_indexes = np.random.choice(indexes, num)

    for idx in sample_indexes:
      tmp_X, tmp_y, tmp_z = dic[key][idx]
      sample_X.append(tmp_X)
      sample_y.append(tmp_y)
      sample_z.append(tmp_z)

  return sample_X, sample_y, sample_z


if __name__ == '__main__':
  train_file = '../data/processed_data/train.pickle'
  dev_file = '../data/processed_data/dev.pickle'
  test_file = '../data/processed_data/test.pickle'
  model_path = '../tmp/combined_filtered_data_union_neural_lstm_augmentation.model'

  with open(train_file, 'rb') as f:
    X_train_f, y_train_f, z_train_f = pickle.load(f)
    X_train, y_train, z_train = getSample(X_train_f, y_train_f, z_train_f)
    print('train: ', len(X_train))

  with open(dev_file, 'rb') as f:
    X_dev, y_dev, z_dev = pickle.load(f)

  with open(test_file, 'rb') as f:
    X_test, y_test, z_test = pickle.load(f)


  dataVarification(X_train, y_train)
  '''
  X_train = np.asarray(X_train).astype(np.float32)
  y_train = np.asarray(y_train).astype(np.float32)
  X_dev = np.asarray(X_dev).astype(np.float32)
  y_dev = np.asarray(y_dev).astype(np.float32)
  X_test = np.asarray(X_test).astype(np.float32)
  y_test = np.asarray(y_test).astype(np.float32)
  '''

  model = None
  if os.path.exists(model_path):
    print('~~~~~ reusing existing model')
    model = tf.keras.models.load_model(model_path)
  else:
    print('~~~~~ creating new model')
    input_dim_first = len(X_train[0])
    input_dim_second = len(X_train[0][0])

    print(len(X_train), input_dim_first, input_dim_second)
    model = tf.keras.Sequential([
      tf.keras.layers.InputLayer(input_shape=(input_dim_first, input_dim_second)),
      tf.keras.layers.LayerNormalization(),
      tf.keras.layers.LSTM(
        1024,
        activation='softmax',
        kernel_initializer=tf.keras.initializers.GlorotNormal(),
        kernel_regularizer='l2',
      ),
      tf.keras.layers.LayerNormalization(),
      tf.keras.layers.Dense(
        1024,
        activation='softmax',
        kernel_initializer=tf.keras.initializers.GlorotNormal(),
        kernel_regularizer='l2',
      ),
      tf.keras.layers.LayerNormalization(),
      tf.keras.layers.Dense(
        7,
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

  print('~~~~~ start training model')
  model.fit(X_train, y_train, epochs=500, batch_size=32)
  model.save(model_path)

  print(model.evaluate(X_train, y_train))
  print(model.evaluate(X_dev, y_dev))
