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
def loadPatchesFromPath(path: str):
    """
    This function loads patches from a given path, and gives labels to the patches from the same path.

    Parameters:
    path (str): Path to folder with patches.

    Returns:
    list: The loaded patches with the labels.
    """
    dataset = []
    patches_count = 0  # For logging
    shape_type = path.split("/")[-1]
    try:
        classes = os.listdir(path)
    except FileNotFoundError:
        print(f"[{inspect.stack()[0][3]}] - Output file {path} not found.")
        return
    for c in classes:
        patches = os.listdir(os.path.join(path, c))
        print(f"Collecting patches from {os.path.join(path, c)}")
        for i, patch in enumerate(patches):
            img = maintain_aspect_ratio_resize(cv2.imread(os.path.join(path, c, patch), 0), 250, 250)
            progress(i + 1, len(patches))

            dataset.append(tuple((img, CLASSES_VALUE_MAIN_MODEL[shape_type])))
            patches_count += 1
    print(f"collected dataset: of {shape_type}")
    return dataset


def buildData(input_dir, dirr):
    """
    This function builds the data from the output folders.

    Parameters:
    runCrop (bool): Cache flag.

    Returns:
    tuple: a tuple where tuple[0] is a list of the data and tuple[1] is the classes of the data.
    """
    start_time = datetime.now()
    print(f"[{inspect.stack()[0][3]}] - Start building data for the Neural Network.")
    if not os.path.exists(os.path.join(PROJECT_DIR, dirr)):
        dirr = crop.main(input_dir, dirr)  # PreProcessing run
    try:
        output_folders = os.listdir(dirr)
    except FileNotFoundError:
        print(f"[{inspect.stack()[0][3]}] - Output file {str(crop.OUTPUT_PATH)} not found.")
        exit(1)

    dataset = []
    for name in output_folders:
        print(f"[{inspect.stack()[0][3]}] - Loading patches from {name} Folder.")
        dataset += loadPatchesFromPath(os.path.join(dirr, name))  # Append the patches list from each output folder
        print(f"[{inspect.stack()[0][3]}] - Finished loading from {name} Folder.")
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


def curr_time():
    curr_time = datetime.now()
    return f"{str(curr_time.date())}-{str(curr_time.hour)}.{str(curr_time.minute)}"
