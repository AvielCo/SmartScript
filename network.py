from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten

from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.layers import Dense , Conv1D,MaxPooling1D , LSTM , Embedding, Dropout, Flatten
from keras.layers import Bidirectional
from keras.models import Sequential
from keras.callbacks import TensorBoard
from keras.optimizers import rmsprop
from keras.models import load_model


############################# RAN's EDIT #############################
from cv2 import cv2
import os
import random
import crop
from datetime import datetime

# Get data after the PreProcessing
def loadPatchesFromPath(path: str):
        dataset = []
        ashkenazi = True
        if not path[path.rfind('/') + 1:].startswith('A'): # Starts with 'A' means Ashkenazi script
               ashkenazi = False
        try:
                patchesNames = os.listdir(path)
        except FileNotFoundError:
                crop.logging.error("Input file '" + path + "' not found.")
                return
        for patch in patchesNames:
                dataset.append(tuple((cv2.imread(os.path.join(path, patch)), ashkenazi)))
        return dataset

def shuffleDataset(dataset: list):
        return random.shuffle(dataset)

def splitDataset(dataset: list):
        data, validations = zip(*dataset)
        return list(data), list(validations)

def buildData():
        startTime = datetime.now()
        crop.logging.info("Start to build the data for the Neural Network.")
        crop.main() # PreProcessing run
        try:
                inputFolders = os.listdir(crop.inputFolder)
        except FileNotFoundError:
                crop.logging.error("Input file '" + str(crop.inputFolder) + "' not found.")
                exit(1)
        dataset = []
        for name in inputFolders:
                dataset += loadPatchesFromPath(os.path.join(crop.inputFolder, name))
        dataset, validations = splitDataset(shuffleDataset(dataset))
        crop.logging.info("Data build ended, execution time: " + str(datetime.now() - startTime))
        return dataset, validations

buildData()

############################# UNTIL HERE #############################

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