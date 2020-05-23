import os
import logging
import inspect
from pytz import timezone
import concurrent.futures
from datetime import datetime, timedelta
from cv2 import cv2
import subprocess

# Global variables
NUM_OF_CROPPED_IMAGES=0
NUM_OF_PATCHES=0
# Threads
NUM_OF_THREADS=2

# Logger
tz = timezone('Asia/Jerusalem')
handlers = [logging.FileHandler('logs/' + str(datetime.now(tz).strftime("%d-%m_%H:%M:%S")) + '_logger.log', mode="w"), logging.StreamHandler()]
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s - %(message)s', datefmt="%d/%m/%y - %H:%M:%S",
                    handlers=handlers)

def timetz(*args):
    return datetime.now(tz).timetuple()

logging.Formatter.converter = timetz

# Dirs
PROJECT_DIR = os.getcwd()
INPUT_PATH = os.path.join(PROJECT_DIR, "input")
OUTPUT_PATH = os.path.join(PROJECT_DIR, "output")

# Page details
# Single page dimensions
CROP_DIMENSIONS = {"A1": {"x1": 1000, "y1": 350, "x2": 2750, "y2": 2800, "margin": 200, "pageNum": 2},
                  "A2": {"x1": 1000, "y1": 550, "x2": 3300, "y2": 3650, "margin": 800, "pageNum": 2},
                  "A3": {"x1": 1000, "y1": 700, "x2": 3200, "y2":3750, "margin": 700, "pageNum": 2},
                  "A4": {"x1": 2450, "y1": 1200, "x2": 5200, "y2":5900, "margin": 1000, "pageNum": 2},
                  "B1": {"x1": 700, "y1": 400, "x2": 2800, "y2": 3600, "margin": 300, "pageNum": 2},
                  "B2": {"x1": 180, "y1": 130, "x2": 1600, "y2": 2200, "margin": 330, "pageNum": 2},
                  "B3": {"x1": 950, "y1": 400, "x2": 2900, "y2": 2850, "margin": 350, "pageNum": 2}, 
                  "I": {"x1": 750, "y1": 700, "x2": 3200, "y2": 4500, "margin": 0, "pageNum": 1},
                  "S": {"x1": 1250, "y1": 925, "x2": 3025, "y2":3700, "margin": 400, "pageNum": 2}
                  }

PATCH_DIMENSIONS = {"x": 300, "y": 200, "xOffset": 300 // 3, "yOffset": 200 // 3}


def getMinResolution():
    """
    This function returns the minimum resolution of the cropDimesions dict.

    Returns:
    dict: The minimum height and width.
    """
    height = width = 200000
    for key in CROP_DIMENSIONS.keys():
        if CROP_DIMENSIONS[key]["x2"] - CROP_DIMENSIONS[key]["x1"] < width:
            width = CROP_DIMENSIONS[key]["x2"] - CROP_DIMENSIONS[key]["x1"]
        if CROP_DIMENSIONS[key]["y2"] - CROP_DIMENSIONS[key]["y1"] < height:
            height = CROP_DIMENSIONS[key]["y2"] - CROP_DIMENSIONS[key]["y1"]
    return {"height": height, "width": width}

RESIZE_UNITS = getMinResolution()

def cropSinglePage(imageName: str, dimensionsDict: dict, folderName: str):
    """
    This function crops a single page from the scan (by its dimensions).

    Parameters:
    imageName (str): The name of the scanned image.
    dimensionsDict (dict): The dimensions of the scanned image.
    folderName (str): The name of the folder that the scan is saved in.
    """
    img = cv2.imread(os.path.join(INPUT_PATH, folderName, imageName), cv2.IMREAD_GRAYSCALE) # Read the image from the folder with grayscale mode
    originalName = imageName # For the log
    x1 = dimensionsDict["x1"]
    x2 = dimensionsDict["x2"]
    y1 = dimensionsDict["y1"]
    y2 = dimensionsDict["y2"]
    delta = dimensionsDict["x2"] - dimensionsDict["x1"] # The offset to move to the next page of the scan
    for _ in range(dimensionsDict["pageNum"]):
        croppedImage = img[y1:y2, x1:x2] # Crop the margins of the image
        croppedImage = cv2.resize(croppedImage, (RESIZE_UNITS["width"], RESIZE_UNITS["height"])) # Resize the image to work with the same size of the manuscript
        saveName = os.path.splitext(imageName)[0]  # Get the name of the image without the extension (e.g. without '.jpg')
        cropToPatches(croppedImage, saveName, RESIZE_UNITS["width"], RESIZE_UNITS["height"], folderName)
        x1 += delta + dimensionsDict["margin"] # Move the X1 axis to the next page
        x2 += delta + dimensionsDict["margin"] # Move the X2 axis to the next page
        imageName = os.path.splitext(imageName)[0] + "2" + os.path.splitext(imageName)[1] # give the second page a different save name
    global NUM_OF_CROPPED_IMAGES
    NUM_OF_CROPPED_IMAGES += 1
    logging.info("[" + inspect.stack()[0][3] + "] - " + "Image " + originalName + " Cropped successfully.")


def cropFiles(imagesInput, dimensionsDict: dict, folderName: str):
    """
    This function calls cropSinglePage for each image in the imagesInput list, with its dimensions and input folder name.

    Parameters:
    imagesInput (list): List of images from the same input folder.
    dimensionsDict (dict): The dimensions of the images.
    folderName (str): Input folder of the images.
    """
    for imageName in imagesInput:
        cropSinglePage(imageName, dimensionsDict, folderName)


def listToChunks(l, n):
    """
    This function divides the images into chunks so that the threads could work on each chunk.

    Prameters:
    l(list): List of images.
    n(int): Number of chunks.

    Returns:
    list: each chunk as a list of images.
    """
    for i in range(0, len(l), n):
        yield l[i:i + n]


def runThreads(folderName: str, dimensionsDict: dict):
    """
    This function creates output folders and runs threads on each chunk of images.

    Parameters:
    folderName(str): The name of the images folder inside output folder.
    dimensionsDict(dict): The dimension of the scanned images.
    """
    path = os.path.join(INPUT_PATH, folderName)
    try:
        imagesInput = os.listdir(path) # Get all of the images from the current folder
    except FileNotFoundError:
        logging.error("[" + inspect.stack()[0][3] + "] - Input file '" + path + "' not found.")
        return
    if not os.path.exists(OUTPUT_PATH): 
        os.mkdir(OUTPUT_PATH) # Create output folder
    if not os.path.exists(os.path.join(OUTPUT_PATH, folderName)): 
        os.mkdir(os.path.join(OUTPUT_PATH, folderName)) # Create a folder inside output folder
    if NUM_OF_THREADS == 1: # Prevent division by zero
        NUM_OF_THREADS += 1
    i = round(len(imagesInput) // (NUM_OF_THREADS - 1))
    chunks = list(listToChunks(imagesInput, i)) # Divide the images into chunks for the threads
    with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_OF_THREADS) as executor: # A thread pool for the threads
        for i in range(NUM_OF_THREADS):
            try:
                executor.submit(cropFiles, chunks[i], dimensionsDict, folderName) # Add thread to the pool with its chunk
            except IndexError:
                continue

def cropToPatches(image, imageName: str, imageWidth: int, imageHeight: int, folderName: str):
    """
    This function takes a page, crops it into patches of 300X200 pixels and saves them in output folder.

    Parameters:
    image (list): List of pixels represented the RBG of the image.
    imageName (str): The name of the image.
    imageWidth (int): The width (X axis) of the image.
    imageHeight (int): The height (Y axis) of the image.
    folderName (str): The name of the output folder.
    """
    x1 = y1 = 0
    x2, y2 = PATCH_DIMENSIONS["x"], PATCH_DIMENSIONS["y"] # The dimension of the patch (current: 300X200)
    xOffset, yOffset = PATCH_DIMENSIONS["xOffset"], PATCH_DIMENSIONS["yOffset"] # The offset of the patch (defined as 1/3 the size of the patch)
    i = 1 # Index for naming each patch
    while x2 < imageWidth: # End of pixels row
        j = 0 # Index for Y axis offset
        while y2 + yOffset * j < imageHeight: # End of pixels col
            croppedPatch = image[y1 + yOffset * j: y2 + yOffset * j, x1: x2] # Extract the pixels of the selected patch
            saveLocation = os.path.join(OUTPUT_PATH, folderName, imageName + "_" + str(i) + ".jpg")
            global NUM_OF_PATCHES
            NUM_OF_PATCHES += 1 # Patches counter
            cv2.imwrite(saveLocation, croppedPatch) # Save the patch to the output folder
            i += 1 
            j += 1
        x1 += xOffset
        x2 += xOffset


def preProcessingMain():
    """
    This function loads the folder names from the input folder and executes the crop algorithm on each name, with its crop dimestions.
    """
    try:
        foldersName = os.listdir(INPUT_PATH) # Folders name from input folder (e.g. "A1", "B1"...)
    except FileNotFoundError:
        logging.error("[" + inspect.stack()[0][3] + "] - Input file '" + INPUT_PATH + "' not found.")
        return # The script can't run without input
    logging.info("[" + inspect.stack()[0][3] + "] - " + "Deleting output folder")
    subprocess.call("rm -rf " + OUTPUT_PATH + os.sep + "*", shell=True) # Delete output folder
    logging.info("[" + inspect.stack()[0][3] + "] - " + "Done")
    for name in foldersName:
        logging.info("[" + inspect.stack()[0][3] + "] - " + "Start cropping the folder " + name + ".")
        try:
            runThreads(name, CROP_DIMENSIONS[name]) # Pass the folder name and its dimensions
            logging.info("[" + inspect.stack()[0][3] + "] - " + "Cropping of " + name + " succeeded.")
        except KeyError:
            logging.error("[" + inspect.stack()[0][3] + "] - File name doesn't match to the dimensions dictionary's key.") # In case the folder name is incorrect,
                                                                                         # or the dimensions dict doesn't contain the folder dimensions
            logging.error("[" + inspect.stack()[0][3] + "] - Cropping of " + name + " Failed.")


def main():
    """
    Main function with execution time logging.
    """
    startTime = datetime.now()
    logging.info("[" + inspect.stack()[0][3] + "] - " + "Crop Script started")
    preProcessingMain()
    logging.info("[" + inspect.stack()[0][3] + "] - " + "Crop Script ended, execution time: " + str(datetime.now() - startTime))
    logging.info("[" + inspect.stack()[0][3] + "] - " + str(NUM_OF_CROPPED_IMAGES) + " Images have been cropped into " + str(NUM_OF_PATCHES) + " Patches.")


if __name__ == "__main__":
    main()
