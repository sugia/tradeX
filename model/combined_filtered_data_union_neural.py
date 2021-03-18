'''
This file trains a multi-class classification neural network model
to classify stock price changes based on unions of financial statements.

Experimental result shows that, after 500 epochs:
the accuracy on training set is 0.8102825284004211;
the accuracy on dev set is 0.7362831830978394;

with only l2:
424/424 [==============================] - 1s 2ms/step - loss: 0.7042 - categorical_accuracy: 0.7383
[0.7041707634925842, 0.7382901906967163]
106/106 [==============================] - 0s 2ms/step - loss: 0.7032 - categorical_accuracy: 0.7428
[0.7032282948493958, 0.7427728772163391]

with only layer norm:
424/424 [==============================] - 1s 2ms/step - loss: 0.1091 - categorical_accuracy: 0.9542
[0.10914360731840134, 0.9541934132575989]
106/106 [==============================] - 0s 3ms/step - loss: 1.3497 - categorical_accuracy: 0.7431
[1.3497074842453003, 0.7430678606033325]

with l2 and layer norm:
424/424 [==============================] - 1s 3ms/step - loss: 0.5280 - categorical_accuracy: 0.7550
[0.5280001163482666, 0.755034327507019]
106/106 [==============================] - 0s 3ms/step - loss: 0.5408 - categorical_accuracy: 0.7555
[0.5408431887626648, 0.7554572224617004]
'''
import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow as tf
import os

if __name__ == '__main__':
  file = '../data/processed_data/combined_filtered_data_union.txt'
  model_path = '../tmp/combined_filtered_data_union_l2_neural_layernorm.model'

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

  model.fit(X_train, y_train, epochs=200, batch_size=32)
  model.save(model_path)

  print(model.evaluate(X_train, y_train))
  print(model.evaluate(X_test, y_test))

