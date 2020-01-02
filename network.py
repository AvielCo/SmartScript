from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten
from keras.utils import to_categorical
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.layers import Dense , Conv1D,MaxPooling1D , LSTM , Embedding, Dropout, Flatten
from keras.layers import Bidirectional
from keras.models import Sequential
from keras.callbacks import TensorBoard
from keras.optimizers import rmsprop
from keras.models import load_model
import numpy as np
from cv2 import cv2
import os
import random
import crop
from datetime import datetime
from sklearn.model_selection import train_test_split

trainPercent = 0.7
testPercent = 1 - trainPercent

# Get data after the PreProcessing
def loadPatchesFromPath(path: str):
        dataset = []
        ashkenazi = True
        if not path[path.rfind('/') + 1:].startswith('A'): # Starts with 'A' means Ashkenazi script
               ashkenazi = False
        try:
                patchesNames = os.listdir(path)
        except FileNotFoundError:
                crop.logging.error("Output file '" + path + "' not found.")
                return
        for patch in patchesNames:
                dataset.append(tuple((cv2.imread(os.path.join(path, patch)), ashkenazi)))
        return dataset

def shuffleDataset(dataset: list):
        random.shuffle(dataset)
        return dataset

def splitDataset(dataset: list):

        data, classes = zip(*dataset)
        return list(data), list(classes)

def buildData(cacheFlag=False):
        startTime = datetime.now()
        crop.logging.info("Start to build the data for the Neural Network.")
        if not cacheFlag:
                crop.main() # PreProcessing run
        try:
                outputFolders = os.listdir(crop.outputFolder)
        except FileNotFoundError:
                crop.logging.error("Output file '" + str(crop.outputFolder) + "' not found.")
                exit(1)
        dataset = []
        for name in outputFolders:
                dataset += loadPatchesFromPath(os.path.join(crop.outputFolder, name))
        dataset, classes = splitDataset(shuffleDataset(dataset))
        crop.logging.info("Data build ended, execution time: " + str(datetime.now() - startTime))
        return dataset, classes


df, y = buildData(False)
df = np.asarray(df)
y = to_categorical(y)
print("HI")

print(y)
X_train, X_test, y_train, y_test = train_test_split(df, y, test_size=testPercent)

#create model
model = Sequential()
#add model layers
model.add(Conv2D(64, kernel_size=3, activation="relu", input_shape=(df.shape[1],df.shape[2], df.shape[3])))
model.add(Flatten())
model.add(Dense(1, activation="softmax"))

        #save the best model
checkpiont=ModelCheckpoint('test1.h5', monitor='val_loss', verbose=1, save_best_only=True,
                                   save_weights_only=True, mode='auto', period=1)
tensorboard = TensorBoard(log_dir='./logs/test1', histogram_freq=2,write_graph=True, write_images=True)
model.compile(loss='binary_crossentropy',
                      optimizer="SGD",
                      metrics=['accuracy'])

model.fit(X_train, y_train, validation_data=(X_test, y_test),batch_size=32, validation_split=0.2,
                       epochs=100, verbose=2, callbacks=[checkpiont] )

#model.fit(X_train, y_train,
#                       batch_size=32, validation_split=0.2,
#                       epochs=100, verbose=2, callbacks=[tensorboard, checkpiont])
scores = model.evaluate(X_test, y_test, verbose=1)
print("Test accuracy:" , scores[1]*100)