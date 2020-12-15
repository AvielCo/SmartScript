import inspect
from datetime import datetime

import cv2
import numpy as np
from PIL import Image
from PIL import UnidentifiedImageError

from consts import *
from dual_print import dual_print

total_images_cropped = 0
total_patches_cropped = 0


def countPixels(img):
    n = PATCH_DIMENSIONS["x"] // 2
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


def is_good_patch(cropped_patch):
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


def crop_image_to_patches(bw_img, grayscale_img, image_width, image_height, image_name, folder_name, shape_type):
    """
    This function takes a page, crops it into patches of 400x400 pixels and saves them in output folder.

    Parameters:
    image (list): List of pixels represented the RBG of the image.
    imageName (str): The name of the image.
    imageWidth (int): The width (X axis) of the image.
    imageHeight (int): The height (Y axis) of the image.
    folderName (str): The name of the output folder.
    """
    if shape_type is not None:
        items_in_folder = len(os.listdir(os.path.join(OUTPUT_PATH, shape_type, folder_name)))
        if shape_type == "cursive" and items_in_folder >= 8000:
            return False
        if shape_type != "cursive" and items_in_folder >= 4000:
            return False
    global total_images_cropped
    global total_patches_cropped
    x1 = y1 = 0
    x2, y2 = PATCH_DIMENSIONS["x"], PATCH_DIMENSIONS["y"]  # The dimension of the patch (current: 400X400)
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
                                             f"{total_patches_cropped}_{i}.jpg"  # image_i.jpg
                                             )  # save location: output\\shape_type\\folder_name\\image_name_i.jpg

            else:
                save_location = os.path.join(os.getcwd(),
                                             PREDICT_OUTPUT_PATH,
                                             folder_name,
                                             image_name + "_" + str(i) + ".jpg")

            if is_good_patch(bw_cropped_patch):
                total_patches_cropped += 1
                cv2.imwrite(save_location, gray_cropped_patch)  # Save the patch to the output folder
            i += 1
            j += 1
        x1 += x_offset
        x2 += x_offset

    total_images_cropped += 1
    dual_print(f"Successfully cropped to patches {image_name} in {save_location}, with shape: {shape_type}")
    return True


def binarization(img):
    """
    turn rgb image to black and white using thresh hold.
    Args:
        img: an image to crop to patches.
    Returns: image that has been processed
    """
    img = cv2.medianBlur(img, 13)
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    return img


def crop_image_edges(image_path):
    img_path = os.path.join(BUFFER_PATH, "buffer_img.jpg")
    if os.path.exists(img_path):
        os.remove(img_path)
    img_path_left = os.path.join(BUFFER_PATH, "buffer_img_1.jpg")
    img_path_right = os.path.join(BUFFER_PATH, "buffer_img_2.jpg")
    try:
        os.remove(img_path_left)
    except FileNotFoundError:
        pass
    try:
        os.remove(img_path_right)
    except FileNotFoundError:
        pass
    Image.MAX_IMAGE_PIXELS = None
    try:
        img = Image.open(image_path)
    except UnidentifiedImageError:
        new_path = image_path.rsplit(path_delimiter, 1)[0]
        new_path += "/new_image.jpg"
        os.rename(image_path,
                  new_path)
    except FileNotFoundError:
        return
    w, h = img.size
    w_c, h_c = 0.10, 0.10
    coords = (w * w_c, h * h_c, w * (1 - w_c), h * (1 - h_c))
    try:
        img = img.crop(coords)
    except OSError:
        return False

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
            dual_print(e, "error")
            return False
    else:  # page has only 1 side
        np_img = np.array(img)
        try:
            cv2.imwrite(img_path, cv2.cvtColor(np_img, cv2.COLOR_RGB2BGR))
        except cv2.error as e:
            dual_print(e, "error")
            return False
    return True


def process_image(path: str, folder_name: str, image_name: str, shape_type=None):
    """
    This function process an image
        1. remove the edges of the image
        2. saves both sides of the image if the image has two pages
        3. turn it to black and white using binarization
        4. crop the image (to grayscale patches) using the function crop_to_patches
    Parameters:
    imageName (str): The name of the scanned image.
    folderName (str): The name of the folder that the scan is saved in.
    """
    buffer_path = BUFFER_PATH
    full_img_path = os.path.join(path, folder_name, image_name)
    t = True
    if not crop_image_edges(full_img_path):
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
            bw_img = binarization(grayscale_img)  # Open pic in BW

            t = crop_image_to_patches(bw_img, grayscale_img, w, h, image_name_no_extension, folder_name, shape_type)
            i += 1
            if not t:
                return t
            dual_print(f"[{inspect.stack()[0][3]}] - Image {image_name_no_extension} Cropped successfully.")
        os.remove(full_img_path)
    return t


def crop_files(images_input, folder_name: str, path: str):
    """
    This function calls cropSinglePage for each image in the imagesInput list, with its dimensions and input folder name

    Parameters:
    imagesInput (list): List of patches from the same input folder.
    dimensionsDict (dict): The dimensions of the patches.
    folderName (str): Input folder of the patches.
    """
    for image_name in images_input:
        shape_type = path.split(path_delimiter)[-1]
        t = process_image(path, folder_name, image_name, shape_type=shape_type)
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
    except FileNotFoundError:
        dual_print(f"[{inspect.stack()[0][3]}] - Input file {input_path} not found.")
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

    crop_files(images_input, folder_name, input_path)


def preProcessingMain(input_dir):
    """
    start the pre processing for the training of the model
    Args:
        input_dir: might be one of the following:
                    1. "input"
                    2. "input/cursive"
                    3. "input/semi_square"
                    4. "input/square"
    """
    folders_names = []
    try:
        # Folders name from input folder (e.g. "AshkenaziCursive", "BizantyCursive"...)
        for dirr in os.listdir(input_dir):
            folders_names.append(os.path.join(input_dir, dirr))

    except FileNotFoundError:
        dual_print(f"[{inspect.stack()[0][3]}] - Input file {INPUT_PATH} not found.", "error")
        return  # The script can"t run without input
    for input_path in folders_names:
        for subdir, dirs, files in os.walk(input_path):
            if files:  # folder doesn"t contains folder(s) => is internal folder (eg: Ashkenazi, Byzantine, Italian...)
                pass
            else:
                for cur_dir in dirs:  # folder contains folder(s) => is external folder (eg: Cursive, Square or Semi Square)
                    dual_print(
                        f"[{inspect.stack()[0][3]}] - Start cropping the folder {os.path.join(subdir, cur_dir)}.")
                    runThreads(subdir, cur_dir, input_path.split(path_delimiter)[-1])
                    dual_print(f"[{inspect.stack()[0][3]}] - Done cropping {os.path.join(subdir, cur_dir)}")


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


def main(input_dir, output_dir: str = ""):
    """
    Main function with execution time logging.
    """
    start_time = datetime.now()
    dual_print(f"[{inspect.stack()[0][3]}] - Crop Script started")
    createFolders()
    preProcessingMain(input_dir)

    if len(output_dir) > 0:
        os.rename(os.path.join(PROJECT_DIR, "output"), os.path.join(PROJECT_DIR, output_dir))
    else:
        import time
        time.sleep(1)
        i = 0
        while True:
            if os.path.exists(os.path.join(PROJECT_DIR, f"output_{i}")):
                i += 1
                continue
            os.rename(os.path.join(PROJECT_DIR, "output"), os.path.join(PROJECT_DIR, f"output_{i}"))
            output_dir = f"output_{i}"
            break

    dual_print(f"[{inspect.stack()[0][3]}] - Crop Script ended, execution time: {str(datetime.now() - start_time)}")
    dual_print(
        f"[{inspect.stack()[0][3]}] - {str(total_images_cropped)} Images have been cropped into {str(total_patches_cropped)} Patches.")
    return output_dir
