import inspect
import sys
from datetime import datetime

import cv2

import crop
from consts import *


def splitDataset(dataset: list):
    """
    This function splits the dataset into data and classes (labels).

    Parameters:
    dataset (list): The dataset.

    Returns:
    tuple: A tuple where tuple[0] is a list of the data and tuple[1] is the classes of the data.
    """
    data, classes = zip(*dataset)
    return list(data), list(classes)


# Get data after the PreProcessing
def loadPatchesFromPath(path: str, model_type=MAIN_MODEL):
    """
    This function loads patches from a given path, and gives labels to the patches from the same path.

    Parameters:
    path (str): Path to folder with patches.

    Returns:
    list: The loaded patches with the labels.
    """
    dataset = []
    patches_count = 0  # For logging
    font = path.split(path_delimiter)[-1]

    try:
        classes = os.listdir(path)
    except FileNotFoundError:
        print(f"[{inspect.stack()[0][3]}] - Output file {path} not found.")
        return

    for origin_type in classes:
        class_type = font if model_type == MAIN_MODEL else origin_type
        patches = os.listdir(os.path.join(path, origin_type))
        print(f"Collecting patches from {os.path.join(path, origin_type)}")
        for i, patch in enumerate(patches):
            img = maintain_aspect_ratio_resize(cv2.imread(os.path.join(path, origin_type, patch), 0), 224, 224)
            progress(i + 1, len(patches))

            dataset.append(tuple((img, CLASSES[model_type][class_type])))
            patches_count += 1
    print(f"collected dataset: of {class_type}")

    return dataset


def buildData(model_type, output_dir):
    """
    This function builds the data from the output folders.

    Parameters:
    runCrop (bool): Cache flag.

    Returns:
    tuple: a tuple where tuple[0] is a list of the data and tuple[1] is the classes of the data.
    """
    start_time = datetime.now()
    print(f"[{inspect.stack()[0][3]}] - Start building data for the Neural Network.")
    if not os.path.exists(os.path.join(PROJECT_DIR, output_dir)):
        output_dir = crop.main("input", output_dir)  # PreProcessing run
    try:
        output_folders = os.listdir(output_dir)  # output_folder => ['cursive', 'square', 'semi_square']
    except FileNotFoundError:
        print(f"[{inspect.stack()[0][3]}] - Output file {str(crop.OUTPUT_PATH)} not found.")
        exit(1)

    dataset = []
    if model_type in output_folders:
        # model_type == one of 'cursive' or 'square' or 'semi_square
        # meaning: training the second layer models
        dataset += loadPatchesFromPath(os.path.join(output_dir, model_type), model_type)

    # dataset = [ (img1, 0), (img2, 1) ... ]

    else:
        # model_type == "main"
        # meaning: training the first layer model
        for folder_type in output_folders:
            print(f"[{inspect.stack()[0][3]}] - Loading patches from {folder_type} Folder.")
            dataset += loadPatchesFromPath(
                os.path.join(output_dir, folder_type))  # Append the patches list from each output folder
            print(f"[{inspect.stack()[0][3]}] - Finished loading from {folder_type} Folder.")

    # Dataset is X, classes (labels) are Y
    dataset, classes = splitDataset(dataset)
    print(f"[{inspect.stack()[0][3]}] - Data build ended, execution time: {str(datetime.now() - start_time)}")
    return dataset, classes


def progress(count, total, suffix=""):
    """
    Showing progress bar on loops
    Args:
        count: current iteration
        total: total iterations
        suffix: ""

    Returns: None
    """

    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = "=" * filled_len + "-" * (bar_len - filled_len)

    sys.stdout.write("[%s] %s%s ...%s\r" % (bar, percents, "%", suffix))
    sys.stdout.flush()  # As suggested by Rom Ruben


def maintain_aspect_ratio_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    # Grab the image size and initialize dimensions
    dim = None
    (h, w) = image.shape[:2]

    # Return original image if no need to resize
    if width is None and height is None:
        return image

    # We are resizing height if width is none
    if width is None:
        # Calculate the ratio of the height and construct the dimensions
        r = height / float(h)
        dim = (int(w * r), height)
    # We are resizing width if height is none
    else:
        # Calculate the ratio of the width and construct the dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # Return the resized image
    return cv2.resize(image, dim, interpolation=inter)
