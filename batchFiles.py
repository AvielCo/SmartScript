import os
import random
from datetime import datetime

import cv2
import numpy as np
from keras.models import load_model
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split

import crop

trainPercent = 0.7
testPercent = 1 - trainPercent


# Get data after the PreProcessing
def loadPatchesFromPath(path: str):
    dataset = []
    ashkenazi = True
    if not path[path.rfind(os.path.sep) + 1:].startswith('A'):  # Starts with 'A' means Ashkenazi script
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
        crop.main()  # PreProcessing run
    try:
        outputFolders = os.listdir(crop.outputFolder)
    except FileNotFoundError:
        crop.logging.error("Output file '" + str(crop.outputFolder) + "' not found.")
        exit(1)
    dataset = []
    for name in outputFolders:
        dataset += loadPatchesFromPath(os.path.join(crop.outputFolder, name))
    # datasets are X, labels are y
    dataset, classes = splitDataset(shuffleDataset(dataset))
    crop.logging.info("Data build ended, execution time: " + str(datetime.now() - startTime))
    return dataset, classes


df, y = buildData(True)
df = np.asarray(df)
y = to_categorical(y)
X_train, X_test, y_train, y_test = train_test_split(df, y, test_size=testPercent, random_state=42)

# create model
model = load_model('test1.h5')

model.fit(X_train, y_train, validation_data=(X_test, y_test), batch_size=32, validation_split=0.2, epochs=32)

scores = model.evaluate(X_test, y_test, verbose=1)
print("Test accuracy: ", scores[1] * 100)
crop.logging.info("Test accuracy: " + str(scores[1] * 100))
