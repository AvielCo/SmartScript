import inspect
import logging
from datetime import datetime

import cv2
import numpy as np
from PIL import Image
from PIL import UnidentifiedImageError

from consts import *

total_images_cropped = 0
total_patches_cropped = 0


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
    delta_white = 0.10
    count = 0
    for i in range(len(black_pixels_avg)):
        if black_pixels_avg[i] < delta_white:
            count += 1
        if black_pixels_avg[i] > delta_black:
            count += 1
        if count >= 2:
            return False
    return True


def cropToPatches(bw_img, grayscale_img, image_width, image_height, image_name, folder_name, shape_type):
    """
    This function takes a page, crops it into patches of 400x400 pixels and saves them in output folder.

    Parameters:
    image (list): List of pixels represented the RBG of the image.
    imageName (str): The name of the image.
    imageWidth (int): The width (X axis) of the image.
    imageHeight (int): The height (Y axis) of the image.
    folderName (str): The name of the output folder.
    """
    items_in_folder = len(os.listdir(os.path.join(OUTPUT_PATH, shape_type, folder_name)))
    if shape_type == 'cursive' and items_in_folder >= 4000:
        return False
    if shape_type != 'cursive' and items_in_folder >= 2000:
        return False
    global total_images_cropped
    global total_patches_cropped
    x1 = y1 = 0
    x2, y2 = PATCH_DIMENSIONS["x"], PATCH_DIMENSIONS["y"]  # The dimension of the patch (current: 500X500)
    x_offset, y_offset = PATCH_DIMENSIONS["xOffset"], PATCH_DIMENSIONS[
        "yOffset"]  # The offset of the patch (defined as 1/2 the size of the patch)
    save_location = str
    i = 1  # Index for naming each patch
    while x2 < image_width:  # End of pixels row
        j = 0  # Index for Y axis offset
        while y2 + y_offset * j < image_height:  # End of pixels col
            bw_cropped_patch = bw_img[y1 + y_offset * j: y2 + y_offset * j,
                               x1: x2]  # Extract the pixels of the selected patch
            gray_cropped_patch = grayscale_img[y1 + y_offset * j: y2 + y_offset * j,
                                 x1: x2]
            if shape_type is not None:
                save_location = os.path.join(OUTPUT_PATH,
                                             shape_type,  # cursive / square / semi square
                                             folder_name,  # for example AshkenaziCursive
                                             str(total_patches_cropped) + "_" + str(i) + ".jpg"  # image_i.jpg
                                             )  # save location: output\\shape_type\\folder_name\\image_name_i.jpg

            else:
                save_location = os.path.join(os.getcwd(),
                                             PREDICT_OUTPUT_PATH,
                                             folder_name,
                                             image_name + "_" + str(i) + ".jpg")
            if isGoodPatch(bw_cropped_patch):
                total_patches_cropped += 1
                cv2.imwrite(save_location, gray_cropped_patch)  # Save the patch to the output folder
            i += 1
            j += 1
        x1 += x_offset
        x2 += x_offset

    total_images_cropped += 1
    print(f"Successfully cropped to patches {image_name} in {save_location}, with shape: {shape_type}")
    return True


def RGBtoBW(img):
    '''
    turn rgb image to black and white using thresh hold.
    Args:
        img: an image to crop to patches.
    Returns: image that has been processed
    '''
    img = cv2.medianBlur(img, 13)
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    return img


def cropImageEdges(image_path, is_predict):
    if not is_predict:
        path = BUFFER_PATH
    else:
        path = PREDICT_BUFFER_PATH

    img_path = os.path.join(path, "buffer_img.jpg")
    if os.path.exists(img_path):
        os.remove(img_path)
    img_path_left = os.path.join(path, "buffer_img_1.jpg")
    img_path_right = os.path.join(path, "buffer_img_2.jpg")
    if os.path.exists(img_path_left) or os.path.exists(img_path_right):
        os.remove(img_path_left)
        os.remove(img_path_right)

    Image.MAX_IMAGE_PIXELS = None
    try:
        img = Image.open(image_path)
    except UnidentifiedImageError:
        new_path = image_path.rsplit('\\', 1)[0]
        new_path += '\\new_image.jpg'
        os.rename(image_path,
                  new_path)
    except FileNotFoundError:
        return
    w, h = img.size
    w_c, h_c = 0.10, 0.10
    coords = (w * w_c, h * h_c, w * (1 - w_c), h * (1 - h_c))
    img = img.crop(coords)
    w, h = img.size
    ratio = h / w
    if ratio < 1:  # page has 2 sides, so we have to divide them into 2 files, each has its own page
        left = (0, 0, w / 2 - ((w / 2) * 0.03), h)
        right = (w / 2 + ((w / 2) * 0.03), 0, w, h)
        left_side = np.array(img.crop(left))
        right_side = np.array(img.crop(right))
        try:
            cv2.imwrite(img_path_left, cv2.cvtColor(left_side, cv2.COLOR_RGB2BGR))
            cv2.imwrite(img_path_right, cv2.cvtColor(right_side, cv2.COLOR_RGB2BGR))
        except cv2.error as e:
            print(e)
            return False
    else:  # page has only 1 side
        np_img = np.array(img)
        try:
            cv2.imwrite(img_path, cv2.cvtColor(np_img, cv2.COLOR_RGB2BGR))
        except cv2.error as e:
            print(e)
            return False
    return True


def cropSinglePage(path: str, folder_name: str, image_name: str, is_predict=False):
    """
    This function crops a single page from the scan (by its dimensions).

    Parameters:
    imageName (str): The name of the scanned image.
    folderName (str): The name of the folder that the scan is saved in.
    """
    if is_predict:
        buffer_path = PREDICT_BUFFER_PATH
        shape_type = None
        full_img_path = os.path.join(os.getcwd(), path, folder_name, image_name)
    else:
        buffer_path = BUFFER_PATH
        shape_type = path.split('\\')[-1]
        full_img_path = os.path.join(path, folder_name, image_name)
    t = True
    if not cropImageEdges(full_img_path, is_predict):
        os.remove(full_img_path)
        return t
    for _, _, files in os.walk(buffer_path):
        i = 0
        for file in files:
            file_path = os.path.join(buffer_path, file)
            grayscale_img = cv2.imread(file_path, 0)  # Read the image from the folder with grayscale mode
            image_name_no_extension = os.path.splitext(image_name)[0]  # For the log
            if i == 0:
                image_name_no_extension = image_name_no_extension + "_left"
            else:
                image_name_no_extension = image_name_no_extension + "_right"
            dims = grayscale_img.shape
            h, w = dims[0], dims[1]
            bw_img = RGBtoBW(grayscale_img)  # Open pic in BW
            t = cropToPatches(bw_img, grayscale_img, w, h, image_name_no_extension, folder_name, shape_type)
            i += 1
            if not t:
                return t
            print(f"[{inspect.stack()[0][3]}] - Image {image_name_no_extension} Cropped successfully.")
    if not is_predict:
        os.remove(full_img_path)
    return t


def cropFiles(images_input, folder_name: str, path: str):
    """
    This function calls cropSinglePage for each image in the imagesInput list, with its dimensions and input folder name

    Parameters:
    imagesInput (list): List of patches from the same input folder.
    dimensionsDict (dict): The dimensions of the patches.
    folderName (str): Input folder of the patches.
    """
    for image_name in images_input:
        t = cropSinglePage(path, folder_name, image_name)
        if not t:
            return


def runThreads(input_path: str, folder_name: str, type_):
    """
    This function creates output folders and runs threads on each chunk of patches.

    Parameters:
    folderName(str): The name of the patches folder inside output folder.
    """
    full_input_path = os.path.join(input_path, folder_name)
    try:
        images_input = os.listdir(full_input_path)  # Get all of the patches from the current folder
        for img in images_input:
            "".join(img.split())
    except FileNotFoundError:
        print(f"[{inspect.stack()[0][3]}] - Input file '{input_path}' not found.")
        return

    output_path = ""
    if type_ == CURSIVE:
        output_path = os.path.join(CURSIVE_OUTPUT_PATH, folder_name)
    elif type_ == SQUARE:
        output_path = os.path.join(SQUARE_OUTPUT_PATH, folder_name)
    elif type_ == SEMI_SQUARE:
        output_path = os.path.join(SEMI_SQUARE_OUTPUT_PATH, folder_name)

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    cropFiles(images_input, folder_name, input_path)


def preProcessingMain(input_dir):
    """
    This function loads the folder names from the input folder and executes the crop algorithm on each name, with its
     crop dimensions.
    """
    folders_names = []
    try:
        # Folders name from input folder (e.g. "AshkenaziCursive", "BizantyCursive"...)
        for dirr in os.listdir(input_dir):
            folders_names.append(os.path.join(input_dir, dirr))

    except FileNotFoundError:
        logging.error(f"[{inspect.stack()[0][3]}] - Input file '{INPUT_PATH}' not found.")
        return  # The script can't run without input
    for input_path in folders_names:
        for subdir, dirs, files in os.walk(input_path):
            if files:  # folder doesn't contains folder(s) => is internal folder (eg: Ashkenazi, Byzantine, Italian...)
                pass
            else:
                for cur_dir in dirs:  # folder contains folder(s) => is external folder (eg: Cursive, Square or Semi Square)
                    print(f"[{inspect.stack()[0][3]}] - Start cropping the folder {os.path.join(subdir, cur_dir)}.")
                    runThreads(subdir, cur_dir, input_path.split('\\')[-1])
                    print(f"[{inspect.stack()[0][3]}] - Done cropping {os.path.join(subdir, cur_dir)}")


def createFolders():
    # CREATE OUTPUT PATHS
    if not os.path.exists(CURSIVE_OUTPUT_PATH):
        os.makedirs(CURSIVE_OUTPUT_PATH)
    if not os.path.exists(SQUARE_OUTPUT_PATH):
        os.makedirs(SQUARE_OUTPUT_PATH)
    if not os.path.exists(SEMI_SQUARE_OUTPUT_PATH):
        os.makedirs(SEMI_SQUARE_OUTPUT_PATH)

    if not os.path.exists(BUFFER_PATH):
        os.makedirs(BUFFER_PATH)


def main(input_dir):
    """
    Main function with execution time logging.
    """
    start_time = datetime.now()
    print(f"[{inspect.stack()[0][3]}] - Crop Script started")
    createFolders()
    preProcessingMain(input_dir)
    print(f"[{inspect.stack()[0][3]}] - Crop Script ended, execution time: {str(datetime.now() - start_time)}")
    print(
        f"[{inspect.stack()[0][3]}] - {str(total_images_cropped)} Images have been cropped into {str(total_patches_cropped)} Patches.")
