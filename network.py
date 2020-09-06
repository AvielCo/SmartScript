import gc
import inspect
import os
import random
import sys
from datetime import datetime

import cv2
import numpy as np
from keras_preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
from tensorflow.compat.v1 import InteractiveSession, ConfigProto
# Deep learning imports
from tensorflow.keras import optimizers
from tensorflow.keras.callbacks import TensorBoard, ModelCheckpoint
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten
from tensorflow.keras.models import Sequential
from tensorflow.keras.utils import to_categorical

import crop

trainPercent = 0.7
testPercent = 1 - trainPercent

# GPU configuration
config = ConfigProto()
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)

CLASSES_VALUE = {'cursive': 0, 'semi_square': 1, 'square': 2}


# Get data after the PreProcessing
def loadPatchesFromPath(path: str):
    """
    This function loads patches from a given path, and gives labels to the patches from the same path.

    Parameters:
    path (str): Path to folder with patches.

    Returns:
    list: The loaded patches with the labels.
    """
    dataset = []
    patches_count = 0  # For logging
    shape_type = path.split('\\')[-1]
    try:
        classes = os.listdir(path)
    except FileNotFoundError:
        crop.logging.error("[" + inspect.stack()[0][3] + "] - Output file '" + path + "' not found.")
        return
    for c in classes:
        patches = os.listdir(os.path.join(path, c))
        for patch in patches:
            patches_count += 1
            dataset.append(tuple((cv2.imread(os.path.join(path, c, patch), 0), CLASSES_VALUE[shape_type])))
    print('collected dataset: of {}'.format(shape_type))
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
        crop.main()  # PreProcessing run
    try:
        outputFolders = os.listdir(crop.OUTPUT_PATH)
    except FileNotFoundError:
        crop.logging.error("[" + inspect.stack()[0][3] + "] - Output file '" + str(crop.outputFolder) + "' not found.")
        exit(1)

    dataset = []
    for name in outputFolders:
        crop.logging.info("[" + inspect.stack()[0][3] + "] - Loading patches from " + name + " Folder.")
        dataset += loadPatchesFromPath(
            os.path.join(crop.OUTPUT_PATH, name))  # Append the patches list from each output folder
        crop.logging.info("[" + inspect.stack()[0][3] + "] - Finished loading from " + name + " Folder.")
    # Dataset is X, classes (labels) are Y
    dataset, classes = splitDataset(shuffleDataset(dataset))
    crop.logging.info(
        "[" + inspect.stack()[0][3] + "] - Data build ended, execution time: " + str(datetime.now() - startTime))
    return dataset, classes


# Cache flag from command line
try:
    runCrop = False
    if sys.argv[1] == "True" or sys.argv[1] == "true":
        runCrop = True
except IndexError:
    pass

df1, y1 = buildData(runCrop)  # True = Starting crop process
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
df = df.reshape((df.shape[0], df.shape[1], df.shape[2], 1))
crop.logging.info("Done")
crop.logging.info("Converting Y to categorical matrix")
# 0 1 2 3...
# 1 0 0 ...
# 0 0 1 ...
# 0 1 0 ...
y = to_categorical(y1)
crop.logging.info("Calling Garbage Collector")
del y1
gc.collect()
crop.logging.info("Done")
crop.logging.info("Splitting data into train and test")
X_train, X_test, y_train, y_test = train_test_split(df, y, test_size=testPercent, random_state=42)
inputShape = (df.shape[1], df.shape[2], df.shape[3])
crop.logging.info("Calling Garbage Collector")
del y
del df
gc.collect()
crop.logging.info("Done")

# Create model
model = Sequential()

# Add model layers
crop.logging.info("Adding model layers")
model.add(Conv2D(64, (3, 3), activation="sigmoid", input_shape=inputShape))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(32, (3, 3), activation="sigmoid", input_shape=inputShape))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(32, (3, 3), activation="sigmoid", input_shape=inputShape))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(64, (3, 3), activation="relu", input_shape=inputShape))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())

model.add(Dense(units=128, activation='sigmoid'))
model.add(Dense(units=128, activation='sigmoid'))
model.add(Dense(units=64, activation='relu'))
model.add(Dense(units=32, activation='sigmoid'))
model.add(Dense(units=3, activation="softmax"))

# Save the best model
crop.logging.info("Creating checkpoint")
checkpoint = ModelCheckpoint('test.h5', monitor='val_acc', verbose=1, save_best_only=True,
                             save_weights_only=True, mode='auto', save_freq=1)

logDir = "logs/fit/" + datetime.now().strftime("%d-%m_%H:%M:%S")
tensorboard = TensorBoard(log_dir=logDir, histogram_freq=1, write_graph=True, write_images=True)

adam = optimizers.Adam(lr=0.0001)

crop.logging.info("Compiling model")
model.compile(loss="categorical_crossentropy",
              optimizer=adam,
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
          steps_per_epoch=len(X_train) // batchSize,
          epochs=5,
          validation_data=test_set,
          validation_steps=1000)
crop.logging.info("Done")
crop.logging.info("Running validation")
model.fit(X_train, y_train, validation_data=(X_test, y_test), batch_size=batchSize, epochs=16, verbose=2,
          callbacks=[checkpoint,
                     tensorboard]
          )
scores = model.evaluate(X_test, y_test, verbose=1)
crop.logging.info("Done")
crop.logging.info("Test accuracy: " + str(scores[1] * 100))
model.save('model_test.h5')