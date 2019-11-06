from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten

from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.layers import Dense , Conv1D,MaxPooling1D , LSTM , Embedding, Dropout, Flatten
from keras.layers import Bidirectional
from keras.models import Sequential
from keras.callbacks import TensorBoard
from keras.optimizers import rmsprop
from keras.models import load_model

#create model
model = Sequential()
#add model layers
model.add(Conv2D(64, kernel_size=3, activation="relu", input_shape=(1500,2000,1)))
model.add(Flatten())
model.add(Dense(1, activation="softmax"))


        #save the best model
checkpiont=ModelCheckpoint('test1.h5', monitor='val_loss', verbose=1, save_best_only=True,
                                   save_weights_only=True, mode='auto', period=1)
tensorboard = TensorBoard(log_dir='./logs/test1', histogram_freq=2,write_graph=True, write_images=True)
model.compile(loss='binary_crossentropy',
                      optimizer="SGD",
                      metrics=['accuracy'])
model.fit(self.preprocess['X_train'], self.preprocess['Y_train'],
                       batch_size=32, validation_split=0.2,
                       epochs=100, verbose=2, callbacks=[tensorboard,checkpiont])
scores = self.model.evaluate(self.preprocess['X_test'], self.preprocess['Y_test'], verbose=1)
print("Test accuracy:" , scores[1]*100)