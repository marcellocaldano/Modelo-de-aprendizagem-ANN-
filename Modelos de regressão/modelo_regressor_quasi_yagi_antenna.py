# -*- coding: utf-8 -*-
"""Modelo_Regressor_Quasi_Yagi_Antenna.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/10gKIEbfh6T57msOznkyq7LlbFYgdaE7b
"""

import numpy as np
from numpy import sqrt

import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import KFold
from keras import optimizers
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras import activations
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D, Activation, LeakyReLU
#from autokeras import StructuredDataRegressor
from sklearn.metrics import mean_squared_error,mean_absolute_error
from keras.layers import Dropout
from sklearn.model_selection import RepeatedKFold
from keras.callbacks import EarlyStopping
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import MinMaxScaler
from keras.optimizers import SGD,RMSprop,Adamax,Ftrl,Nadam,Adam

from numpy import asarray
from pandas import read_csv
from sklearn.model_selection import train_test_split
#from autokeras import StructuredDataRegressor
from numpy import asarray
from timeit import default_timer as timer

new_model = tf.keras.models.load_model('Modelo_Quasi_Yagi_Antenna.h5')

df1=pd.read_excel('Quasi-yagi L5 e Lp dataset.xlsx')
df2=pd.read_excel('Quasi-yagi L5 e Lp dataset (1).xlsx')
df=pd.concat([df1,df2])
data=df.copy()
data = df.drop_duplicates()

x=data.drop(labels=['f1', 'f2','f3'],axis=1)
y=data[['f1', 'f2','f3']]

from sklearn.ensemble import IsolationForest
iso_forest = IsolationForest(n_estimators=400, contamination=0.5,random_state=1000)

iso_forest = iso_forest.fit(data)
isof_outliers = iso_forest.predict(data)

isoF_outliers_values = data[iso_forest.predict(data) == -1]

data = data.drop(isoF_outliers_values.index.values.tolist())

x = data.drop(labels=['f1', 'f2', 'f3'], axis=1) 
y = data[[ 'f1', 'f2', 'f3']]

X_train,X_test,y_train,y_test=train_test_split(x,y,test_size=0.30,random_state=7000)
print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)
n_features = X_train.shape[1]

std = StandardScaler()
#std = MinMaxScaler()
#x_std=std.fit_transform(x)
X_train_std = std.fit_transform(X_train)
X_test_std = std.transform(X_test)

Y_train_std = std.fit_transform(y_train)
Y_test_std = std.transform(y_test)

es = EarlyStopping(monitor='val_loss', mode='min', verbose=0, patience=400)



neuron=1024
model=Sequential()
#model.add(Dropout(0.2,input_shape=(n_features,)))
model.add(Dense(32,input_shape=(n_features,), activation='relu', kernel_initializer=tf.keras.initializers.GlorotNormal()))
model.add(Dense(256, activation='relu', kernel_initializer=tf.keras.initializers.GlorotNormal()))
#model.add(Dense(32, activation='relu', kernel_initializer=tf.keras.initializers.GlorotNormal()))
##model.add(Dense(256, activation='relu', kernel_initializer=tf.keras.initializers.GlorotNormal()))
#model.add(Dense(256, activation='relu', kernel_initializer=tf.keras.initializers.HeNormal))
#model.add(Dense(neuron, activation='relu', kernel_initializer=tf.keras.initializers.HeNormal))
#model.add(Dense(neuron, activation='relu', kernel_initializer=tf.keras.initializers.HeNormal))
#model.add(Dense(neuron, activation='relu', kernel_initializer=tf.keras.initializers.HeNormal))
#model.add(Dropout(0.4))





model.add(Dense(3))

opt = Adam(learning_rate=0.001)#,momentum=0.5)

model.compile(optimizer=opt, metrics=[keras.metrics.MeanSquaredError()], loss='mse')
  




start = timer()


history=model.fit(X_train_std, Y_train_std, epochs=6000,validation_data=(X_test_std,Y_test_std), batch_size=256,callbacks=[es], verbose=0)

end = timer()
print(end - start) # Time in seconds, e.g. 5.38091952400282

model.summary( )

from matplotlib import pyplot
#pyplot.subplot(211)
plt.figure(figsize=(20,10))
pyplot.title('Cross-Entropy Loss', pad=-40)
pyplot.plot(history.history['loss'], label='train')
pyplot.plot(history.history['val_loss'], label='test')

pyplot.legend()

yhat =model.predict(X_test_std)
yhat=std.inverse_transform(yhat)
mse = (mean_squared_error(y_test, yhat))
rmse = (mean_squared_error(y_test, yhat,squared=False))
mae = (mean_absolute_error(y_test, yhat))
print('MSE = ',mse,'RMSE = ',rmse, 'MAE = ', mae)

preds= model.predict(X_test_std)
preds=std.inverse_transform(preds)
rmse = (mean_squared_error(y_test.values[:,0], preds[:,0]))
print(rmse)

preds= model.predict(X_test_std)
preds=std.inverse_transform(preds)
rmse = (mean_squared_error(y_test.values[:,1], preds[:,1]))
print(rmse)

preds= new_model.predict(X_test_std)
preds=std.inverse_transform(preds)
rmse = (mean_squared_error(y_test.values[:,2], preds[:,2]))
print(rmse)

def plot_target_var(var_name, var_indx, y_true, y_pred):
    if var_indx is not None:
      target_true = y_true[:, var_indx]
      target_pred = y_pred[:, var_indx]

    else:
      target_true = y_true
      target_pred = y_pred


    fig, ax = plt.subplots(figsize=(20,10))
    ax.scatter(target_true, target_pred)
    ax.plot([target_true.min(),target_true.max()], [target_true.min(), target_true.max()], 'k--', lw=4)
    ax.set_xlabel('Measured')
    ax.set_ylabel('Predicted')
    plt.title(var_name)
    for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
                ax.get_xticklabels() + ax.get_yticklabels()):
        item.set_fontsize(20)
    plt.show()

plot_target_var(var_name='f1', var_indx=0, y_true=y_test.values,y_pred=preds)

plot_target_var(var_name='f2', var_indx=1, y_true=y_test.values,y_pred=preds)

plot_target_var(var_name='f3', var_indx=2, y_true=y_test.values,y_pred=preds)

model.save('Modelo_Quasi_Yagi_Antenna.h5')