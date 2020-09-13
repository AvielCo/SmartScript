import random
import sys
from datetime import datetime

import cv2


def shuffleDataset(dataset: list):
    """
    This function shuffles the dataset.

    Parameters:
    dataset (list): The dataset.

    Returns:
    list: The shuffled dataset.
    """
    random.shuffle(dataset)
    return dataset


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


def progress(count, total, suffix=''):
    """
    Showing progress bar on loops
    Args:
        count: current iteration
        total: total iterations
        suffix: ''

    Returns: None
    """

    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
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
    return str(curr_time.date()) + '-' + str(curr_time.hour) + '.' + str(curr_time.minute)
