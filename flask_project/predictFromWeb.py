import os
import shutil

import cv2
import numpy as np
from tensorflow.keras.models import load_model

from consts import PREDICT_OUTPUT_PATH
from crop import cropSinglePage
from general import maintain_aspect_ratio_resize

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
PATCHES_PATH = "patches"
MODEL_NAME = os.path.join(os.getcwd(), 'BestModel.h5')

CLASSES_VALUE = {"cursive": 0, "semi_square": 1, "square": 2}


class BColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Get data after the PreProcessing
def loadPatchesFromPath(path: str):
    dataset = []
    try:
        patchesNames = os.listdir(path)
    except FileNotFoundError:
        return
    for patch in patchesNames:
        img = maintain_aspect_ratio_resize(cv2.imread(os.path.join(path, patch), 0), 227, 227)
        dataset.append(img)
    return dataset


def buildData(folderID, crop):
    if not os.path.exists(os.path.join(PREDICT_OUTPUT_PATH, folderID)):
        os.makedirs(os.path.join(PREDICT_OUTPUT_PATH, folderID))

    # take the first image, there always gonna be 1 image so its safe
    img = os.listdir(os.path.join("raw_images", folderID))[0]

    # crop the image
    if crop:
        cropSinglePage("raw_images", folderID, img, is_predict=True)

    dataset = loadPatchesFromPath(os.path.join("patches", folderID))
    return dataset


def runPredict(folderID):
    model = load_model(MODEL_NAME)
    df = buildData(folderID, crop=True)
    df = np.asarray(df)
    df = df.reshape((df.shape[0], df.shape[1], df.shape[2], 1))
    summ = [0, 0, 0]
    print("Predicting {} patches...".format(len(df)))
    prediction = model.predict(df, batch_size=1, verbose=0, steps=None)
    for p in prediction:
        p0, p1, p2 = summ
        summ = p[0] + p0, p[1] + p1, p[2] + p2

    max_val = max(summ)
    print(f"{BColors.OKGREEN}")
    if max_val == summ[0]:
        print("Done!\nCursive: {}%".format((summ[0] * 100) / len(prediction)))
    elif max_val == summ[1]:
        print("Done!\nSemi Square: {}%".format((summ[1] * 100) / len(prediction)))
    else:
        print("Done!\nSquare: {}%".format((summ[2] * 100) / len(prediction)))
    print(f"{BColors.ENDC}")
    # shutil.rmtree(os.path.join("patches", folderID))
    # shutil.rmtree(os.path.join("raw_images", folderID))


runPredict("1")
