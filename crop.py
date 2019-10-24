from cv2 import cv2
import os
import logging
from datetime import datetime
# import numpy as np
# import matplotlib.pyplot as plt


# Global variables

# Logger
handlers = [logging.FileHandler('logger.log',mode="w"), logging.StreamHandler()]
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s - %(message)s', datefmt="%H:%M:%S", handlers=handlers)

# Dirs
projectDir = os.getcwd()
inputFolder = os.path.join(projectDir, "input")
outputFolder = os.path.join(projectDir, "output")

# Page details

# Single page dimensions
cropDimensions = {"x1": 1200, "y1": 400, "x2": 2700, "y2": 2400 }
# Pages middle margin
margin = 150


def cropSinglePage(imageName: str):
    img = cv2.imread(os.path.join(inputFolder, imageName), cv2.IMREAD_GRAYSCALE)
    originalName = imageName
    x1 = cropDimensions["x1"]
    x2 = cropDimensions["x2"]
    y1 = cropDimensions["y1"]
    y2 = cropDimensions["y2"]
    for _ in range(2):
        croppedImage = img[y1:y2, x1:x2]
        saveLocation = os.path.join(outputFolder, imageName + ".jpg")
        cv2.imwrite(saveLocation, croppedImage)
        delta = cropDimensions["x2"] - cropDimensions["x1"]
        x1 += delta + margin
        x2 += delta + margin
        imageName += "2"
    logging.info("Image " +  originalName + " Cropped successfully.")

def main():
    imagesInput = os.listdir(inputFolder)
    for imageName in imagesInput:
        cropSinglePage(imageName)

if __name__ == "__main__":
    startTime = datetime.now()
    logging.info("Script started")
    main()
    logging.info("Script ended, execution time: " + str(datetime.now() - startTime))
