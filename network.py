import os
import gc
import sys
import crop
import random
import inspect
import numpy as np
from cv2 import cv2
from datetime import datetime

# Deep learning imports
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import optimizers
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from keras_preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import load_model, Sequential
from tensorflow.compat.v1 import InteractiveSession, ConfigProto
from tensorflow.keras.callbacks import TensorBoard, CSVLogger, ModelCheckpoint, EarlyStopping
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, LSTM, Embedding, Dropout, Flatten

trainPercent = 0.7
testPercent = 1 - trainPercent

# GPU configuration
config = ConfigProto()
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)


# Get data after the PreProcessing
def loadPatchesFromPath(path: str):
        """
        This function loads patches from a given path, and gives labels (boolean of Ashkenazi or not) to the patches from the same path.

        Parameters:
        path (str): Path to folder with patches.

        Returns:
        list: The loaded patches with the labels.
        """
        dataset = []
        ashkenazi = True # Default value for label
        patchesCount = 0 # For logging
        if not path[path.rfind(os.path.sep) + 1:].startswith('A'): # Starts with 'A' means Ashkenazi script
                ashkenazi = False
        try:
                patchesNames = os.listdir(path)
                patchesNum = len(patchesNames)
        except FileNotFoundError:
                crop.logging.error("[" + inspect.stack()[0][3] + "] - Output file '" + path + "' not found.")
                return 
        for patch in patchesNames:
                patchesCount += 1
                dataset.append(tuple((cv2.imread(os.path.join(path, patch), cv2.IMREAD_GRAYSCALE), ashkenazi))) # Append a tuple of a single patch with its label
                if patchesCount % 10000 == 0: # For the logger
                    crop.logging.info("[" + inspect.stack()[0][3] + "] - Loaded " + str(patchesCount) + "/" + str(patchesNum) + " Patches from " + os.path.basename(path) + ".")
        return dataset

def shuffleDataset(dataset: list):
        """
        This function shuffles the dataset.

        Parameters:
        dataset (list): The dataset.

        Returns:
        list: The shuffled dataset.
        """
        random.shuffle(dataset)
        return dataset

def splitDataset(dataset: list):
        """
        This function splits the dataset into data and classes (labels).

        Parameters:
        dataset (list): The dataset.

        Returns:
        tuple: A tuple where tuple[0] is a list of the data and tuple[1] is the classes of the data.
        """
        data, classes = zip(*dataset)
        return list(data), list(classes)



def buildData(runCrop=False):
        """
        This function builds the data from the output folders.

        Parameters:
        runCrop (bool): Cache flag.

        Returns:
        tuple: a tuple where tuple[0] is a list of the data and tuple[1] is the classes of the data.
        """
        startTime = datetime.now()
        crop.logging.info("[" + inspect.stack()[0][3] + "] - Starting to build the data for the Neural Network.")
        if runCrop:
                crop.main() # PreProcessing run
        try:
                outputFolders = os.listdir(crop.outputFolder)
        except FileNotFoundError:
                crop.logging.error("[" + inspect.stack()[0][3] + "] - Output file '" + str(crop.outputFolder) + "' not found.")
                exit(1)

        dataset = []
        for name in outputFolders:
                crop.logging.info("[" + inspect.stack()[0][3] + "] - Loading patches from " + name + " Folder.")
                dataset += loadPatchesFromPath(os.path.join(crop.outputFolder, name)) # Append the patches list from each output folder
                crop.logging.info("[" + inspect.stack()[0][3] + "] - Finished loading from " + name + " Folder.")
        # Dataset is X, classes (labels) are Y
        dataset, classes = splitDataset(shuffleDataset(dataset))
        crop.logging.info("[" + inspect.stack()[0][3] + "] - Data build ended, execution time: " + str(datetime.now() - startTime))
        return dataset, classes

# Cache flag from command line
try:
        runCrop = False
        if sys.argv[1] == "True" or sys.argv[1] == "true":
                runCrop = True
except IndexError:
        pass

df1, y1 = buildData(runCrop) # True = Starting crop process
crop.logging.info("Calling Garbage Collector")
gc.collect()
crop.logging.info("Done")
crop.logging.info("Converting data to Numpy array")
df = np.asarray(df1)
crop.logging.info("Calling Garbage Collector")
del df1
gc.collect()
crop.logging.info("Done")
crop.logging.info("Reshaping Grayscale data for Conv2D dimesions")
df = df.reshape(df.shape[0], df.shape[1], df.shape[2], 1)
crop.logging.info("Done")
crop.logging.info("Converting Y to categorical matrix")
y = to_categorical(y1)
crop.logging.info("Calling Garbage Collector")
del y1
gc.collect()
crop.logging.info("Done")
crop.logging.info("Splitting data into train and test")
X_train, X_test, y_train, y_test = train_test_split(df, y, test_size=testPercent, random_state=42)
inputShape = (df.shape[1],df.shape[2], df.shape[3])
crop.logging.info("Calling Garbage Collector")
del y
del df
gc.collect()
crop.logging.info("Done")

# Create model
model = Sequential()

# Add model layers
crop.logging.info("Adding model layers")
model.add(Conv2D(64,(3,3), activation="sigmoid", input_shape=inputShape ))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Conv2D(32,(3,3), activation="sigmoid", input_shape=inputShape))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Conv2D(32,(3,3), activation="sigmoid", input_shape=inputShape))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Conv2D(64,(3,3), activation="relu", input_shape=inputShape))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Flatten())

model.add(Dense(units = 128, activation = 'sigmoid'))
model.add(Dense(units = 128, activation = 'sigmoid'))
model.add(Dense(units = 64, activation = 'relu'))
model.add(Dense(units = 32, activation = 'sigmoid'))
model.add(Dense(units = 2, activation="softmax"))

# Save the best model
crop.logging.info("Creating checkpoint")
checkpoint = ModelCheckpoint('test1.h5', monitor='val_acc', verbose=1, save_best_only=True,
                                   save_weights_only=True, mode='auto', period=1)

logDir="logs/fit/" + datetime.now().strftime("%d-%m_%H:%M:%S")
tensorboard = TensorBoard(log_dir=logDir, histogram_freq=1,write_graph=True, write_images=True)


adam = optimizers.Adam(lr=0.0001)

crop.logging.info("Compiling model")
model.compile( loss = "binary_crossentropy",
               optimizer = adam,
               metrics=['accuracy']
             )

# Fit arguments
crop.logging.info("Fitting arguments:")
crop.logging.info("Fit train datagen")
train_datagen = ImageDataGenerator()
crop.logging.info("Done")
crop.logging.info("Fit test datagen")
test_datagen = ImageDataGenerator()
crop.logging.info("Done")
crop.logging.info("Fit training set")
training_set = train_datagen.flow(X_train, y=y_train)
crop.logging.info("Done")
crop.logging.info("Fit test set")
test_set = test_datagen.flow(X_test, y=y_test)
crop.logging.info("Done")
crop.logging.info("Model summary:")
model.summary(print_fn=crop.logging.info)
crop.logging.info("Running the model")
batchSize = 128
model.fit(training_set,
		steps_per_epoch = len(X_train)//batchSize,
		epochs = 16,
		validation_data = test_set,
		validation_steps = 2000)
crop.logging.info("Done")
crop.logging.info("Running validation")
model.fit(X_train, y_train, validation_data=(X_test, y_test),batch_size=batchSize, validation_split=0.2,
                               epochs=16, verbose=2, callbacks=[checkpoint, tensorboard] )
scores = model.evaluate(X_test, y_test, verbose=1)
crop.logging.info("Done")
crop.logging.info("Test accuracy: " + str(scores[1] * 100))