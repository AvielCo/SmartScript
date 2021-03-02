import logging
import os
from datetime import datetime

from cv2 import cv2

# Global variables
numOfImagesCropped = 0
numOfPatches = 0

# Dirs
projectDir = os.getcwd()
inputFolder = os.path.join(projectDir, "patches")
outputFolder = os.path.join(projectDir, "patches")

# Dirs
INPUT_PATH = os.path.join(PROJECT_DIR, "input")
OUTPUT_PATH = os.path.join(PROJECT_DIR, "output")
CURSIVE = "cursive"
SEMI_SQUARE = "semi_square"
SQUARE = "square"
CURSIVE_INPUT_PATH = os.path.join(INPUT_PATH, CURSIVE)
SEMI_SQUARE_INPUT_PATH = os.path.join(INPUT_PATH, SEMI_SQUARE)
SQUARE_INPUT_PATH = os.path.join(INPUT_PATH, SQUARE)
CURSIVE_OUTPUT_PATH = os.path.join(OUTPUT_PATH, CURSIVE)
SEMI_SQUARE_OUTPUT_PATH = os.path.join(OUTPUT_PATH, SEMI_SQUARE)
SQUARE_OUTPUT_PATH = os.path.join(OUTPUT_PATH, SQUARE)
BUFFER_PATH = os.path.join(PROJECT_DIR, "buffer")
BUFFER_IMG_PATH = os.path.join(BUFFER_PATH, "buffer_img.jpg")

# Page details

patchDimensions = {"x": 300, "y": 200, "xOffset": 100, "yOffset": 200 // 3}

RESIZE_UNITS = {"height": 2070, "width": 1420}


def cropSinglePage(imageName: str, folderName: str):
    img = cv2.imread(os.path.join(inputFolder, folderName, imageName), cv2.IMREAD_GRAYSCALE)
    originalName = imageName
    croppedImage = cv2.resize(img, (RESIZE_UNITS["width"], RESIZE_UNITS["height"]))
    saveName = os.path.splitext(imageName)[0]  # Get the name of the image without the extension (e.g. without ".jpg")
    cropToPatches(croppedImage, saveName, RESIZE_UNITS["width"], RESIZE_UNITS["height"], folderName)
    global numOfImagesCropped
    numOfImagesCropped += 1
    print("Image " + originalName + " Cropped successfully.")


def cropFiles(imagesInput, folderName: str):
    for imageName in imagesInput:
        cropSinglePage(imageName, folderName)
        os.remove(os.path.join(inputFolder, folderName, imageName))


def runThreads(folderName: str):
    path = folderName
    try:
        imagesInput = os.listdir(path)
    except FileNotFoundError:
        logging.error("Input file "" + path + "" not found.")
        return
    if not os.path.exists(outputFolder):
        os.mkdir(outputFolder)
    if not os.path.exists(os.path.join(outputFolder, folderName)):
        os.mkdir(os.path.join(outputFolder, folderName))
    cropFiles(imagesInput, folderName)


def cropToPatches(image, imageName: str, xDelta: int, yDelta: int, folderName: str):
    x1 = y1 = 0
    x2, y2 = patchDimensions["x"], patchDimensions["y"]
    xOffset, yOffset = patchDimensions["xOffset"], patchDimensions["yOffset"]
    i = 1
    while x2 < xDelta:
        j = 0
        while y2 + yOffset * j < yDelta:
            croppedPatch = image[y1 + yOffset * j: y2 + yOffset * j, x1: x2]
            saveLocation = os.path.join(outputFolder, folderName, imageName + "_" + str(i) + ".jpg")
            global numOfPatches
            numOfPatches += 1
            cv2.imwrite(saveLocation, croppedPatch)
            i += 1
            j += 1
        x1 += xOffset
        x2 += xOffset


def preProcessingMain(folderID):
    global numOfImagesCropped
    numOfImagesCropped = 0
    global numOfPatches
    numOfPatches = 0
    try:
        folderName = os.path.join(inputFolder, folderID)
    except FileNotFoundError:
        logging.error("Input file "" + os.path.join(inputFolder, folderID) + "" not found.")
        return
    print("Start cropping the folder " + folderName + ".")
    runThreads(folderName)
    print("Cropping of " + folderName + " succeeded.")


def main(folderID):
    startTime = datetime.now()
    print("Crop Script started")
    preProcessingMain(folderID)
    print("Crop Script ended, execution time: " + str(datetime.now() - startTime))
    print(str(numOfImagesCropped) + " Images have been cropped into " + str(numOfPatches) + " Patches.")


if __name__ == "__main__":
    main("123")
