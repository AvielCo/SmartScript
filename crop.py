from cv2 import cv2
import os
import logging
from datetime import datetime
import threading
import concurrent.futures
import numpy as np
# import matplotlib.pyplot as plt


# Global variables

# Logger
handlers = [logging.FileHandler('logger.log',mode="w"), logging.StreamHandler()]
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s - %(message)s', datefmt="%H:%M:%S", handlers=handlers)

# Dirs
projectDir = os.getcwd()
inputFolder = os.path.join(projectDir, "input")
outputFolder = os.path.join(projectDir, "output")
# outputFolder = os.path.join(projectDir, "patches_output")

# Page details

# Single page dimensions
cropDimensions = {"x1": 1200, "y1": 400, "x2": 2700, "y2": 2400 } # 1500 X 2000 px
patchDimensions = {"x": 300, "y": 200, "xOffset": 100, "yOffset": 200//3 }
# Pages middle margin
margin = 150

numOfThreads = 4

def cropSinglePage(imageName: str):
    img = cv2.imread(os.path.join(inputFolder, imageName), cv2.IMREAD_GRAYSCALE)
    originalName = imageName
    x1 = cropDimensions["x1"]
    x2 = cropDimensions["x2"]
    y1 = cropDimensions["y1"]
    y2 = cropDimensions["y2"]
    delta = cropDimensions["x2"] - cropDimensions["x1"]
    for _ in range(2):
        croppedImage = img[y1:y2, x1:x2]
        # saveLocation = os.path.join(outputFolder, imageName)
        cropToPatches(croppedImage, originalName)
        # cv2.imwrite(saveLocation, croppedImage)
        x1 += delta + margin
        x2 += delta + margin
        imageName = imageName[:-4] + "2.jpg"
    logging.info("Image " +  originalName + " Cropped successfully.")

def cropFiles(imagesInput):
    for imageName in imagesInput:
        cropSinglePage(imageName)

def listToChunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

def runThreads():
    try:
        imagesInput = os.listdir(inputFolder)
    except FileNotFoundError:
        logging.error("Input file '" + inputFolder + "' not found.")
        return
    if not os.path.exists(outputFolder):
        os.mkdir(outputFolder)
    i = round(len(imagesInput) // (numOfThreads - 1))
    chunks = list(listToChunks(imagesInput,i))
    with concurrent.futures.ThreadPoolExecutor(max_workers=numOfThreads) as executor:
        for i in range(numOfThreads):
            executor.submit(cropFiles, chunks[i])

def cropToPatches(image, imageName: str):
    # image = cv2.imread(os.path.join(outputFolder, imageName))
    x1 = y1 = 0
    x2 = patchDimensions["x"]
    y2 = patchDimensions["y"]
    xOffset = patchDimensions["xOffset"]
    yOffset = patchDimensions["yOffset"]
    i = 1
    imageName = imageName[:-4]
    while x2 < 1500:
        j = 0
        while y2 + yOffset * j < 2000:
            croppedPatch = image[y1 + yOffset * j : y2 + yOffset * j, x1 : x2]
            saveLocation = os.path.join(outputFolder, imageName + str(i) + ".jpg")
            cv2.imwrite(saveLocation, croppedPatch)
            i += 1
            j += 1
        x1 += xOffset
        x2 += xOffset

# def runPatchesThreads():
#     try:
#         imagesInput = os.listdir(outputFolder)
#     except FileNotFoundError:
#         logging.error("Output file '" + outputFolder + "' not found.")
#         return

if __name__ == "__main__":
    startTime = datetime.now()
    logging.info("Script started")
    runThreads()
    logging.info("Script ended, execution time: " + str(datetime.now() - startTime))
