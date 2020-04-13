import os
import logging
from pytz import timezone
import concurrent.futures
from datetime import datetime, timedelta
from cv2 import cv2
import subprocess

# Global variables

numOfImagesCropped = 0
numOfPatches = 0
# Logger
tz = timezone('Asia/Jerusalem')
handlers = [logging.FileHandler('logs/' + str(datetime.now(tz)) + '_logger.log', mode="w"), logging.StreamHandler()]
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s - %(message)s', datefmt="%d/%m/%y - %H:%M:%S",
                    handlers=handlers)

def timetz(*args):
    return datetime.now(tz).timetuple()
logging.Formatter.converter = timetz

# Dirs
projectDir = os.getcwd()
inputFolder = os.path.join(projectDir, "input")
outputFolder = os.path.join(projectDir, "output")

# Page details

# Single page dimensions

cropDimensions = {"A1": {"x1": 1000, "y1": 350, "x2": 2750, "y2": 2800, "margin": 200, "pageNum": 2},
                  "A2": {"x1": 1000, "y1": 550, "x2": 3300, "y2": 3650, "margin": 800, "pageNum": 2},
                  "B1": {"x1": 700, "y1": 400, "x2": 2800, "y2": 3600, "margin": 300, "pageNum": 2}, # PNX_MANUSCRIPTS000041052-1_IE73769634
                  "B2": {"x1": 180, "y1": 130, "x2": 1600, "y2": 2200, "margin": 330, "pageNum": 2}, # PNX_MANUSCRIPTS003017087-1_IE70795069
                  "B3": {"x1": 950, "y1": 400, "x2": 2900, "y2": 2850, "margin": 350, "pageNum": 2}, 
                  "I": {"x1": 750, "y1": 700, "x2": 3200, "y2": 4500, "margin": 0, "pageNum": 1},
                  "A3": {"x1": 1000, "y1": 700, "x2": 3200, "y2":3750, "margin": 700, "pageNum": 2}
                  }

patchDimensions = {"x": 300, "y": 200, "xOffset": 100, "yOffset": 200 // 3}

numOfThreads = 2

def getMinResolution():
    height = width = 200000
    for key in cropDimensions.keys():
        if cropDimensions[key]["x2"] - cropDimensions[key]["x1"] < width:
            width = cropDimensions[key]["x2"] - cropDimensions[key]["x1"]
        if cropDimensions[key]["y2"] - cropDimensions[key]["y1"] < height:
            height = cropDimensions[key]["y2"] - cropDimensions[key]["y1"]
    return {"height": height, "width": width}

RESIZE_UNITS = getMinResolution()

def cropSinglePage(imageName: str, dimensionsDict: dict, folderName: str):
    img = cv2.imread(os.path.join(inputFolder, folderName, imageName), cv2.IMREAD_GRAYSCALE)
    originalName = imageName
    x1 = dimensionsDict["x1"]
    x2 = dimensionsDict["x2"]
    y1 = dimensionsDict["y1"]
    y2 = dimensionsDict["y2"]
    delta = dimensionsDict["x2"] - dimensionsDict["x1"]
    for _ in range(dimensionsDict["pageNum"]):
        croppedImage = img[y1:y2, x1:x2]
        croppedImage = cv2.resize(croppedImage, (RESIZE_UNITS["width"], RESIZE_UNITS["height"]))
        saveName = imageName[:-4]  # Get the name of the image without the extension (e.g. without '.jpg')
        cropToPatches(croppedImage, saveName, RESIZE_UNITS["width"], RESIZE_UNITS["height"], folderName)
        x1 += delta + dimensionsDict["margin"]
        x2 += delta + dimensionsDict["margin"]
        imageName = imageName[:-4] + "2.jpg"
    global numOfImagesCropped
    numOfImagesCropped += 1
    logging.info("Image " + originalName + " Cropped successfully.")


def cropFiles(imagesInput, dimensionsDict: dict, folderName: str):
    for imageName in imagesInput:
        cropSinglePage(imageName, dimensionsDict, folderName)


def listToChunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


def runThreads(folderName: str, dimensionsDict: dict):
    path = os.path.join(inputFolder, folderName)
    try:
        imagesInput = os.listdir(path)
    except FileNotFoundError:
        logging.error("Input file '" + path + "' not found.")
        return
    if not os.path.exists(outputFolder):
        os.mkdir(outputFolder)
    if not os.path.exists(os.path.join(outputFolder, folderName)):
        os.mkdir(os.path.join(outputFolder, folderName))
    i = round(len(imagesInput) // (numOfThreads - 1))
    chunks = list(listToChunks(imagesInput, i))
    with concurrent.futures.ThreadPoolExecutor(max_workers=numOfThreads) as executor:
        for i in range(numOfThreads):
            try:
                executor.submit(cropFiles, chunks[i], dimensionsDict, folderName)
            except IndexError:
                continue


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


def preProcessingMain():
    try:
        foldersName = os.listdir(inputFolder)
    except FileNotFoundError:
        logging.error("Input file '" + inputFolder + "' not found.")
        return
    subprocess.call("rm -rf " + outputFolder + os.sep + "*", shell=True)
    for name in foldersName:
        logging.info("Start cropping the folder " + name + ".")
        try:
            runThreads(name, cropDimensions[name])
            logging.info("Cropping of " + name + " succeeded.")
        except KeyError:
            logging.error("File name doesn't match to the dictionary's key.")
            logging.error("Cropping of " + name + " Failed.")


def main():
    startTime = datetime.now()
    logging.info("Crop Script started")
    preProcessingMain()
    logging.info("Crop Script ended, execution time: " + str(datetime.now() - startTime))
    logging.info(str(numOfImagesCropped) + " Images have been cropped into " + str(numOfPatches) + " Patches.")


if __name__ == "__main__":
    main()
