import os
import crop
import random
import numpy as np
from cv2 import cv2
from datetime import datetime
from tensorflow.keras.models import load_model


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
                return
        for patch in patchesNames:
                patchesCount += 1
                dataset.append(tuple((cv2.imread(os.path.join(path, patch), cv2.IMREAD_GRAYSCALE), ashkenazi)))

        return dataset

def splitDataset(dataset: list):
        data, classes = zip(*dataset)
        return list(data)



def buildData(runCrop=True):
        startTime = datetime.now()
        if runCrop:
                crop.main() # PreProcessing run
        try:
                outputFolders = os.listdir(crop.outputFolder)
        except FileNotFoundError:
                exit(1)
        dataset = []
        for name in outputFolders:
                dataset += loadPatchesFromPath(os.path.join(crop.outputFolder, name))
        dataset = splitDataset(dataset)
        return dataset

def runPredict():
        model = load_model('model.h5')
        df1 = buildData()
        df = np.asarray(df1)
        print(df.shape)
        df = df.reshape(df.shape[0], df.shape[1], df.shape[2], 1)
        print(len(df))
        temp=model.predict(df, batch_size=1, verbose=1, steps=None)
        cou1,cou2,sum1,sum2=0,0,0,0
        for i in temp:
                sum1+=i[0]
                sum2+=i[1]
                if(i[0]>i[1]):
                        cou1=cou1+1
                else:
                        cou2=cou2+1
        summ= sum1+sum2
        ashkenazipresents = ((cou2/len(df)) + (sum2/summ)) *0.5
        notAshkenazipresents = ((cou1/len(df)) + (sum1/summ)) *0.5
        print("Ashkenazi % : " + str(ashkenazipresents))
        print("Not Ashkenazi % : " + str(notAshkenazipresents))

if __name__ == "__main__":
    runPredict()
