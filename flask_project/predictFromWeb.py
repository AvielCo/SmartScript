import os
import shutil

import numpy as np
# import cropFromWeb
import cv2
from numpy import argmax
from tensorflow.keras.models import load_model

import crop
PATCHES_PATH = "images"
MODEL_NAME = os.path.join(os.getcwd(), 'bestModel.h5')

CLASSES_VALUE = {"cursive": 0, "semi_square": 1, "square": 2}


# Get data after the PreProcessing
def loadPatchesFromPath(path: str):
    dataset = []
    try:
        patchesNames = os.listdir(path)
    except FileNotFoundError:
        return
    for patch in patchesNames:
        dataset.append(cv2.imread(os.path.join(path, patch), cv2.IMREAD_GRAYSCALE))
    return dataset


def buildData(folderID):
    # crop.main(folderID)
    dataset = loadPatchesFromPath(os.path.join(PATCHES_PATH, folderID))
    return dataset


def runPredict(folderID):
    print(MODEL_NAME)
    model = load_model(MODEL_NAME)
    df = buildData(folderID)
    cv2.imshow(df[0])
    cv2.waitKey(0)
    df = np.asarray(df)
    df = df.reshape((df.shape[0], df.shape[1], df.shape[2], 1))
    prediction = model.predict(df, batch_size=1, verbose=1, steps=None)
    p0, p1, p2 = prediction[0], prediction[1], prediction[2]
    max_val = argmax(prediction)
    if max_val == p0:
        print("Cursive: {}".format(p0) * 100)
    elif max_val == p1:
        print("Semi Square: {}".format(p1) * 100)
    else:
        print("Square: {}".format(p2) * 100)

    shutil.rmtree(os.path.join(PATCHES_PATH, folderID), ignore_errors=True)


runPredict("upload")
