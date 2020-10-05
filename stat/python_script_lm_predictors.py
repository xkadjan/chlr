import numpy
from keras.models import Sequential
from keras.layers import Dense
import keras.optimizers
import matplotlib.pyplot as plt
import random


# load the dataset
train=numpy.loadtxt('train.csv', delimiter=',',skiprows=1)
test=numpy.loadtxt('test.csv', delimiter=',',skiprows=1)

# split into input and output variables
train_input=train[:,numpy.array([5,6,13])]
train_output=train[:,1]

test_input=test[:,numpy.array([5,6,13])]
test_output=test[:,1]

random.seed(2) # Pro opakovatelnost výsledků

# define the keras model
model=Sequential()
model.add(Dense(3, activation='relu'))
model.add(Dense(2, activation='relu'))
model.add(Dense(1, activation='relu'))



# compile the keras model

opt = keras.optimizers.Adam(learning_rate=0.001)

model.compile(loss='mae', optimizer=opt, metrics=['mae'])

# fit the keras model on the dataset

m=model.fit(train_input,train_output,epochs=30000,verbose=1,steps_per_epoch=None)

# erorr plot

plt.plot(m.history['mae'])

# predict values

predicted=model.predict(test_input)
predicted.shape=(37,)

print('Prumerna odchylka testovacich dat:',sum(numpy.abs(predicted-test_output))/37)

# R squared

total_squares=numpy.sum((test_output-numpy.mean(test_output))**2)
residual_squares=numpy.sum((predicted-test_output)**2)
print('Artificial Rsq: ',1-(residual_squares/total_squares))

