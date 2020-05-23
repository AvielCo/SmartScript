import os
import shutil
import random
import numpy as np
import cropFromWeb
from cv2 import cv2
from datetime import datetime
from tensorflow.keras.models import load_model

PATCHES_PATH = "images"
MODEL_NAME = "../model.h5"

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
    cropFromWeb.main(folderID)
    dataset = loadPatchesFromPath(os.path.join(PATCHES_PATH, folderID))
    return dataset

def runPredict(folderID):
    model = load_model(MODEL_NAME)
    df = buildData(folderID)
    df = np.asarray(df)
    df = df.reshape(df.shape[0], df.shape[1], df.shape[2], 1)
    prediction = model.predict(df, batch_size=1, verbose=1, steps=None)
    cou1, cou2, sum1, sum2 = 0, 0, 0, 0
    for i in prediction:
        sum1 += i[0]
        sum2 += i[1]
        if(i[0] > i[1]):
            cou1 = cou1+1
        else:
            cou2 = cou2+1
    summ= sum1+sum2
    ashkenazipresents = ((cou2 / len(df)) + (sum2 / summ)) * 0.5
    notAshkenazipresents = ((cou1 / len(df)) + (sum1 / summ)) * 0.5
    results = {"ashkenazi": str(round(ashkenazipresents * 100, 3)), "notAshkenazi": str(round(notAshkenazipresents * 100, 3))}
    print("Ashkenazi % : " + results["ashkenazi"])
    print("Not Ashkenazi % : " + results["notAshkenazi"])
    shutil.rmtree(os.path.join(PATCHES_PATH, folderID), ignore_errors=True)
    
    return results

# if __name__ == "__main__":
#     print(runPredict("123"))
