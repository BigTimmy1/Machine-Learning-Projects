# -*- coding: utf-8 -*-
"""2406632_Sunspot .ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14z6Doyi52ijfRsPA44iAyLfrn41xT5e0
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import seaborn as sns

import matplotlib.pyplot as plt

# for brevity import specific keras objects
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, SimpleRNN, LSTM, GRU
from sklearn.metrics import mean_squared_error

# for repeatable results:
from tensorflow.random import set_seed
from random import seed

SEED = 3
seed(SEED)
np.random.seed(SEED)
set_seed(SEED)

from google.colab import drive
drive.mount('/content/gdrive')

data = pd.read_csv("/content/gdrive/MyDrive/Colab Notebooks/sunspots_data.csv")

data.head()

data['Month'] = pd.to_datetime(data['Month'])
data

plt.figure(figsize=(12, 6))
plt.plot(data['Month'], data['Sunspot Number'], linestyle='-')
plt.title('Sunspot Number Over Time')
plt.xlabel('Month')
plt.ylabel('Sunspot Number')
plt.grid(True)
plt.show()

# split the data into 80% training sets and 20% testing set
split = 0.8
t_end = int(split*len(data)//1)
len(data), t_end

train_data = data.iloc[:t_end,1].values.reshape(-1,1)
test_data = data.iloc[t_end:,1].values.reshape(-1,1)

# scaling the data between 0 and 1 using minmaxscaler
scaler = MinMaxScaler()
scaler.fit(train_data)
train_data = scaler.transform(train_data)
test_data = scaler.transform(test_data)

# functions splits data sequentially into independent and target variable
# and convert the data to numpy array
def splitSequence(seq, n_steps):
    #Declare X and y as empty list
    X = []
    y = []
    for i in range(len(seq)):
        #get the last index
        lastIndex = i + n_steps
        #if lastIndex is greater than length of sequence then break
        if lastIndex > len(seq) - 1:
            break
        #Create input and output sequence
        seq_X, seq_y = seq[i:lastIndex], seq[lastIndex]
        #append seq_X, seq_y in X and y list
        X.append(seq_X)
        y.append(seq_y)
        pass
    #Convert X and y into numpy array
    X = np.array(X)
    y = np.array(y)

    return X,y

# number of sequential steps for independent and target variables
n_steps = 10

# applying split sequence
X_train, y_train = splitSequence(train_data, n_steps)
X_test, y_test = splitSequence(test_data, n_steps)

X_train.shape, y_train.shape, X_test.shape, y_test.shape

n_features = 1
X_train = X_train.reshape((X_train.shape[0], X_train.shape[1],
    n_features))
X_test = X_test.reshape((X_test.shape[0], X_test.shape[1],
    n_features))

# creating a sequential model architechture
model = Sequential()
model.add(GRU(200, activation='tanh', return_sequences=True,
    input_shape=(n_steps, n_features)))
model.add(SimpleRNN(100, activation='tanh'))
model.add(Dense(50))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='sgd', metrics=['accuracy'])

model.summary()

model.fit(X_train, y_train, epochs=20, verbose=2)

loss = model.evaluate(X_test, y_test, verbose=2)
print(loss)
y_pred_train = model.predict(X_train)
y_pred_test = model.predict(X_test)

# Plotting training set
plt.figure(figsize=(10, 5))
plt.plot(y_train, label='Training Data', color='blue')
plt.plot(y_pred_train, label='Predicted Data', color='orange')
plt.title('Training data vs Predicted')
plt.legend()

plt.show()

# Plotting test set
# plt.subplot(1, 2, 2)

plt.figure(figsize=(10,5))
plt.plot(y_test, label='Test Data', color='blue')
plt.plot(y_pred_test, label='Predicted Data', color='orange')
plt.title('Test data vs Predicted')
plt.legend()

plt.show()