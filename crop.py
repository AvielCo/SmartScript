import concurrent.futures
import inspect
import logging
import os
from datetime import datetime

import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from pytz import timezone

# Global variables
NUM_OF_CROPPED_IMAGES = 0
NUM_OF_PATCHES = 0
# Threads
NUM_OF_THREADS = 2

# Logger
tz = timezone('Asia/Jerusalem')


def timetz(*args):
    return datetime.now(tz).timetuple()


logging.Formatter.converter = timetz

# Dirs
PROJECT_DIR = os.getcwd()
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
BUFFER_PATH = os.path.join(PROJECT_DIR, 'buffer')
BUFFER_IMG_PATH = os.path.join(BUFFER_PATH, 'buffer_img.jpg')

# Patch dimensions
PATCH_DIMENSIONS = {"x": 400, "y": 400, "xOffset": 400 // 2, "yOffset": 400 // 2}


def cropSinglePage(image_name: str, folder_name: str, path: str):
    """
    This function crops a single page from the scan (by its dimensions).

    Parameters:
    imageName (str): The name of the scanned image.
    folderName (str): The name of the folder that the scan is saved in.
    """

    full_img_path = os.path.join(path, folder_name, image_name)
    cropImageEdges(full_img_path)
    img = cv2.imread(BUFFER_IMG_PATH, 0)  # Read the image from the folder with grayscale mode
    image_name_no_extension = os.path.splitext(image_name)[0]  # For the log
    dims = img.shape
    h, w = dims[0], dims[1]
    new_img = RGBtoBW(img)
    cropToPatches(new_img, folder_name, path.split('\\')[-1], image_name_no_extension, w, h)
    logging.info("[" + inspect.stack()[0][3] + "] - " + "Image " + image_name_no_extension + " Cropped successfully.")


def RGBtoBW(img):
    _, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh


def cropImageEdges(image_path):
    Image.MAX_IMAGE_PIXELS = None
    img = Image.open(image_path)
    w, h = img.size
    w_c, h_c = 0.10, 0.10
    coords = (w * w_c, h * h_c, w * (1 - w_c), h * (1 - h_c))
    np_img = np.array(img.crop(coords))
    if os.path.exists(BUFFER_IMG_PATH):
        os.remove(BUFFER_IMG_PATH)
    cv2.imwrite(BUFFER_IMG_PATH, np_img)


def cropFiles(images_input, folder_name: str, path: str):
    """
    This function calls cropSinglePage for each image in the imagesInput list, with its dimensions and input folder name

    Parameters:
    imagesInput (list): List of images from the same input folder.
    dimensionsDict (dict): The dimensions of the images.
    folderName (str): Input folder of the images.
    """
    for image_name in images_input:
        cropSinglePage(image_name, folder_name, path)


def listToChunks(lis, n):
    """
    This function divides the images into chunks so that the threads could work on each chunk.

    Prameters:
    l(list): List of images.
    n(int): Number of chunks.

    Returns:
    list: each chunk as a list of images.
    """
    for i in range(0, len(lis), n):
        yield lis[i:i + n]


def runThreads(input_path: str, folder_name: str):
    #                                        -2          -1
    # input_path example: C:\\...\\project\\input\\cursive
    # folder_name example: AshkenaziCursive
    full_input_path = os.path.join(input_path, folder_name)
    """
    This function creates output folders and runs threads on each chunk of images.

    Parameters:
    folderName(str): The name of the images folder inside output folder.
    """

    try:
        images_input = os.listdir(full_input_path)  # Get all of the images from the current folder
        for img in images_input:
            "".join(img.split())
    except FileNotFoundError:
        logging.error("[" + inspect.stack()[0][3] + "] - Input file '" + input_path + "' not found.")
        return

    output_path = ""
    if input_path == CURSIVE_INPUT_PATH:
        output_path = os.path.join(CURSIVE_OUTPUT_PATH, folder_name)
    elif input_path == SQUARE_INPUT_PATH:
        output_path = os.path.join(SQUARE_OUTPUT_PATH, folder_name)
    elif input_path == SEMI_SQUARE_INPUT_PATH:
        output_path = os.path.join(SEMI_SQUARE_OUTPUT_PATH, folder_name)

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    global NUM_OF_THREADS
    if NUM_OF_THREADS == 1:  # Prevent division by zero
        NUM_OF_THREADS += 1
    i = round(len(images_input) // (NUM_OF_THREADS - 1))
    chunks = list(listToChunks(images_input, i))  # Divide the images into chunks for the threads
    with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_OF_THREADS) as executor:  # A thread pool for the threads
        for i in range(NUM_OF_THREADS):
            try:
                executor.submit(cropFiles, chunks[i], folder_name, input_path)  # Add thread to the pool with its chunk
            except IndexError:
                continue


def cropToPatches(image, folder_name: str, shape_type: str, image_name: str, image_width: int, image_height: int):
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
    x2, y2 = PATCH_DIMENSIONS["x"], PATCH_DIMENSIONS["y"]  # The dimension of the patch (current: 500X500)
    x_offset, y_offset = PATCH_DIMENSIONS["xOffset"], PATCH_DIMENSIONS[
        "yOffset"]  # The offset of the patch (defined as 1/3 the size of the patch)
    save_location = str
    i = 1  # Index for naming each patch
    while x2 < image_width:  # End of pixels row
        j = 0  # Index for Y axis offset
        while y2 + y_offset * j < image_height:  # End of pixels col
            cropped_patch = image[y1 + y_offset * j: y2 + y_offset * j,
                            x1: x2]  # Extract the pixels of the selected patch
            save_location = os.path.join(OUTPUT_PATH,
                                         shape_type,  # cursive / square / semi square
                                         folder_name,  # for example AshkenaziCursive
                                         image_name + "_" + str(i) + ".jpg"  # image_i.jpg
                                         )  # save location: output\\shape_type\\folder_name\\image_name_i.jpg
            global NUM_OF_PATCHES
            NUM_OF_PATCHES += 1  # Patches counter
            if isGoodPatch(cropped_patch):
                cv2.imwrite(save_location, cropped_patch)  # Save the patch to the output folder
            i += 1
            j += 1
        x1 += x_offset
        x2 += x_offset
    print("Successfully cropped to patches {0} in {1}".format(image_name, save_location))


def countPixels(img):
    n = PATCH_DIMENSIONS['x'] // 2
    h, w = img.shape
    split_img = []
    k = 0
    for y in range(0, h, n):
        for x in range(0, w, n):
            y1 = y + n
            x1 = x + n
            split_img.insert(k, img[y: y1, x:x1])
            k += 1

    black_pixels_avg = []
    for i in range(4):
        dark_pixels = n ** 2 - cv2.countNonZero(split_img[i])
        black_pixels_avg.insert(i, dark_pixels / (n ** 2))
    return black_pixels_avg


def isGoodPatch(cropped_patch):
    black_pixels_avg = countPixels(cropped_patch)
    delta_black = 0.25
    delta_white = 0.05
    sub: float
    count = 0
    for i in range(len(black_pixels_avg)):
        if black_pixels_avg[i] < delta_white:
            count += 1
        if black_pixels_avg[i] > delta_black:
            count += 1
        if count >= 2:
            return False
    return True


def preProcessingMain():
    """
    This function loads the folder names from the input folder and executes the crop algorithm on each name, with its crop dimentions.
    """
    folders_names = []
    try:
        # Folders name from input folder (e.g. "AshkenaziCursive", "BizantyCursive"...)
        folders_names.insert(0, CURSIVE_INPUT_PATH)
        folders_names.insert(1, SQUARE_INPUT_PATH)
        folders_names.insert(2, SEMI_SQUARE_INPUT_PATH)
    except FileNotFoundError:
        logging.error("[" + inspect.stack()[0][3] + "] - Input file '" + INPUT_PATH + "' not found.")
        return  # The script can't run without input
    logging.info("[" + inspect.stack()[0][3] + "] - " + "Deleting output folder")
    # subprocess.call("rm -rf " + OUTPUT_PATH + os.sep + "*", shell=True) # Delete output folder
    logging.info("[" + inspect.stack()[0][3] + "] - " + "Done")
    for input_path in folders_names:
        for subdir, dirs, files in os.walk(input_path):
            for cur_dir in dirs:
                logging.info("[" + inspect.stack()[0][3] + "] - " + "Start cropping the folder " + subdir + ".")
                try:
                    runThreads(subdir, cur_dir)
                    logging.info("[" + inspect.stack()[0][3] + "] - " + "Cropping of " + subdir + " succeeded.")
                except KeyError:
                    logging.error("[" + inspect.stack()[0][
                        3] + "] - File name doesn't match to the dimensions dictionary's key.")  # In case the folder name is incorrect,
                    # or the dimensions dict doesn't contain the folder dimensions
                    logging.error("[" + inspect.stack()[0][3] + "] - Cropping of " + subdir + " Failed.")


def createFolders():
    # CREATE INPUT PATHS
    if not os.path.exists(CURSIVE_INPUT_PATH):
        os.makedirs(CURSIVE_INPUT_PATH)
    if not os.path.exists(SQUARE_INPUT_PATH):
        os.makedirs(SQUARE_INPUT_PATH)
    if not os.path.exists(SEMI_SQUARE_INPUT_PATH):
        os.makedirs(SEMI_SQUARE_INPUT_PATH)

    # CREATE OUTPUT PATHS
    if not os.path.exists(CURSIVE_OUTPUT_PATH):
        os.makedirs(CURSIVE_OUTPUT_PATH)
    if not os.path.exists(SQUARE_OUTPUT_PATH):
        os.makedirs(SQUARE_OUTPUT_PATH)
    if not os.path.exists(SEMI_SQUARE_OUTPUT_PATH):
        os.makedirs(SEMI_SQUARE_OUTPUT_PATH)


def main():
    """
    Main function with execution time logging.
    """
    startTime = datetime.now()
    logging.info("[" + inspect.stack()[0][3] + "] - " + "Crop Script started")
    createFolders()
    preProcessingMain()
    logging.info(
        "[" + inspect.stack()[0][3] + "] - " + "Crop Script ended, execution time: " + str(datetime.now() - startTime))
    logging.info(
        "[" + inspect.stack()[0][3] + "] - " + str(NUM_OF_CROPPED_IMAGES) + " Images have been cropped into " + str(
            NUM_OF_PATCHES) + " Patches.")


if __name__ == "__main__":
    main()
