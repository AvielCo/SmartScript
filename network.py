from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten
from keras.utils import to_categorical
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.layers import Dense, Conv2D, MaxPooling2D, LSTM, Embedding, Dropout, Flatten
from keras.layers import Bidirectional
from keras.models import Sequential
from keras.callbacks import TensorBoard
from keras.optimizers import rmsprop
from keras.models import load_model
import numpy as np
from cv2 import cv2
import os
import random
import tensorflow as tf
from keras_preprocessing.image import ImageDataGenerator
from tensorflow import keras

import crop
from datetime import datetime
from sklearn.model_selection import train_test_split
from batchFiles import DataGenerator


trainPercent = 0.7
testPercent = 1 - trainPercent

# Get data after the PreProcessing
def loadPatchesFromPath(path: str):
        dataset = []
        ashkenazi = True
        patchesCount = 0
        if not path[path.rfind(os.path.sep) + 1:].startswith('A'): # Starts with 'A' means Ashkenazi script
                ashkenazi = False
        try:
                patchesNames = os.listdir(path)
                patchesNum = len(patchesNames)
        except FileNotFoundError:
                crop.logging.error("Output file '" + path + "' not found.")
                return
        for patch in patchesNames:
                patchesCount += 1
                dataset.append(tuple((cv2.imread(os.path.join(path, patch)), ashkenazi)))
                if patchesCount % 10000 == 0:
                    crop.logging.info("Loaded " + str(patchesCount) + "/" + str(patchesNum) + " Patches from " + os.path.basename(path) + ".")
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
                crop.logging.info("Loading patches from " + name + " Folder.")
                dataset += loadPatchesFromPath(os.path.join(crop.outputFolder, name))
                crop.logging.info("Finished loading from " + name + " Folder.")
        #datasets are X, labels are y
        dataset, classes = splitDataset(shuffleDataset(dataset))
        crop.logging.info("Data build ended, execution time: " + str(datetime.now() - startTime))
        return dataset, classes

df, y = buildData()
crop.logging.info("Converting data to Numpy array")
df = np.asarray(df)
crop.logging.info("Converting Y to categorical matrix")
y = to_categorical(y)
crop.logging.info("Splitting data to train and test")
X_train, X_test, y_train, y_test = train_test_split(df, y, test_size=testPercent,random_state=42)


#create model
model = Sequential()

#add model layers
model.add(Conv2D(32,(3,3), activation="sigmoid", input_shape=(df.shape[1],df.shape[2], df.shape[3])))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Conv2D(64,(3,3), activation="sigmoid", input_shape=(df.shape[1],df.shape[2], df.shape[3])))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Conv2D(64,(3,3), activation="sigmoid", input_shape=(df.shape[1],df.shape[2], df.shape[3])))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Conv2D(128,(3,3), activation="relu", input_shape=(df.shape[1],df.shape[2], df.shape[3])))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Flatten())

model.add(Dense(units = 256, activation = 'sigmoid'))
model.add(Dense(units = 128, activation = 'sigmoid'))
model.add(Dense(units = 64, activation = 'relu'))
model.add(Dense(units = 32, activation = 'sigmoid'))
model.add(Dense(units = 2, activation="softmax"))

#save the best model
checkpoint = ModelCheckpoint('test1.h5', monitor='val_acc', verbose=1, save_best_only=True,
                                   save_weights_only=True, mode='auto', period=1)

logDir="logs/fit/" + datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard = TensorBoard(log_dir=logDir, histogram_freq=1,write_graph=True, write_images=True)


model.compile( loss = "categorical_crossentropy",
               optimizer = "SGD",
               metrics=['accuracy']
             )





#fit arguments
train_datagen = ImageDataGenerator()
test_datagen = ImageDataGenerator()
training_set = train_datagen.flow(X_train, y= y_train)
test_set = test_datagen.flow(X_test, y=y_test)
model.fit_generator(training_set,
		steps_per_epoch = len(X_train),
		epochs = 32,
		validation_data = test_set,
		validation_steps = 2000)

model.fit(X_train, y_train, validation_data=(X_test, y_test),batch_size=32, validation_split=0.2,
                               epochs=32, verbose=2, callbacks=[checkpoint,tensorboard] )

scores = model.evaluate(X_test, y_test, verbose=1)
print("Test accuracy: ", scores[1]*100)
crop.logging.info("Test accuracy: " + str(scores[1]*100))


