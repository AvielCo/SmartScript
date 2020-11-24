import inspect
import logging as log
from datetime import datetime
from dual_print import dual_print
import cv2
import numpy as np

from consts import *


def get_median_height(input_dir):
    height = []
    total_images = 0
    folders_names = []
    try:
        # Folders name from input folder (e.g. "AshkenaziCursive", "BizantyCursive"...)
        folders_names.insert(0, os.path.join(input_dir, CURSIVE))
        folders_names.insert(1, os.path.join(input_dir, SEMI_SQUARE))
        folders_names.insert(2, os.path.join(input_dir, SQUARE))
    except FileNotFoundError:
        logging.error("[{}] - Input file {} not found.".format(inspect.stack()[0][3], INPUT_PATH))
        return  # The script can"t run without input
    for input_path in folders_names:
        for subdir, dirs, _ in os.walk(input_path):
            for cur_dir in dirs:
                path = os.path.join(input_path, cur_dir)
                for image in os.listdir(path):
                    img_path = os.path.join(path, image)
                    i = cv2.imread(img_path)
                    if i is None:
                        new_img_path = os.path.join(path, str(total_images) + ".jpg")
                        os.rename(img_path, new_img_path)
                        dual_print(f"Error in image: {img_path}, renaming to: {new_img_path}", "error")
                        i = cv2.imread(new_img_path)
                    height.append(i.shape[0])
                    total_images += 1
                    dual_print(f"image num: {total_images}, height: {i.shape[0]}")

    h = np.median(height)
    dual_print(h)
    crop_images(input_dir, int(h))


def crop_images(input_dir, avg_height=4742):
    log.basicConfig(format="%(asctime)s--%(levelname)s: %(message)s",
                    datefmt="%H:%M:%S",
                    filename=f"{datetime.now().strftime('%d-%m-%y--%H-%M')}_crop-images-on={input_dir}_with-height={avg_height}",
                    level=log.INFO)
    folders_names = []
    total_images = 0
    try:
        # Folders name from input folder (e.g. "AshkenaziCursive", "BizantyCursive"...)
        folders_names.insert(0, os.path.join(input_dir, CURSIVE))
        folders_names.insert(1, os.path.join(input_dir, SEMI_SQUARE))
        folders_names.insert(2, os.path.join(input_dir, SQUARE))
    except FileNotFoundError:
        dual_print(f"[{inspect.stack()[0][3]}] - Input file {INPUT_PATH} not found.", "error")
        return  # The script can"t run without input
    for input_path in folders_names:
        for subdir, dirs, _ in os.walk(input_path):
            for cur_dir in dirs:
                path = os.path.join(input_path, cur_dir)
                for image in os.listdir(path):
                    img_path = os.path.join(path, image)
                    i = cv2.imread(img_path)
                    if i is None:
                        new_img_path = os.path.join(path, str(total_images) + ".jpg")
                        dual_print(f"Error in image: {img_path}, renaming to: {new_img_path}", "error")
                        os.rename(img_path, new_img_path)
                        img_path = new_img_path
                        i = cv2.imread(img_path)
                    dual_print(f"\nimage: {img_path}")
                    h, w, _ = i.shape
                    if h == avg_height:
                        total_images += 1
                        continue
                    ratio = h / w
                    dual_print(f"old height: {h}, old width: {w}, ratio: {ratio}")

                    w = avg_height // ratio
                    ratio = avg_height / w
                    dual_print(f"new hight: {avg_height}, new width: {int(w)}, ratio: {ratio}")

                    i = cv2.resize(i, (int(w), avg_height))

                    os.remove(img_path)

                    cv2.imwrite(img_path, i)
                    total_images += 1
    dual_print(f"Done changing height to {total_images} pictures")
