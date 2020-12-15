import cv2
import numpy as np
from tensorflow.keras.models import load_model

from consts import *
from crop import process_image
from general import maintain_aspect_ratio_resize

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
PATCHES_PATH = "patches"
MODEL_NAME = os.path.join(os.getcwd(), "models/main.h5")


# Get data after the PreProcessing
def loadPatchesFromPath(path: str):
    dataset = []
    try:
        patchesNames = os.listdir(path)
    except FileNotFoundError:
        return
    for patch in patchesNames:
        img = maintain_aspect_ratio_resize(cv2.imread(os.path.join(path, patch), 0), 227, 227)
        dataset.append(img)
    return dataset


def build_prediction_dataset(image_path: str):
    prediction_patches_path = os.path.join(PROJECT_DIR, "prediction_patches", "1")
    prediction_image_path = os.path.join(PROJECT_DIR, "predict_images")
    try:
        os.makedirs(prediction_patches_path)
    except FileExistsError:
        pass
    try:
        os.makedirs(prediction_image_path)
    except FileExistsError:
        pass
    image = os.listdir(os.path.join(prediction_image_path, "1"))[0]
    print(image)
    # image_name = image_path.split(path_delimiter)[-1]

    # TODO: fix "1" when have a website
    # TODO: why?: because we want to restrict access to two users from same directory
    # TODO: fuck u Aviel from the future
    process_image(prediction_image_path, "1", image)
    dataset = loadPatchesFromPath(os.path.join(prediction_patches_path, "1"))
    return dataset


def run_predict(model_type):
    model = load_model(os.path.join(MODELS_DIR, f"{model_type}.h5"))
    dataset = build_prediction_dataset(os.path.join(PROJECT_DIR, "predict_images", "1"))
    dataset = np.asarray(dataset)
    dataset = dataset.reshape((dataset.shape[0], dataset.shape[1], dataset.shape[2], 1))
    summ = [0, 0, 0]
    print("Predicting {} patches...".format(len(dataset)))
    prediction = model.predict(dataset, batch_size=1, verbose=0, steps=None)
    for p in prediction:
        p0, p1, p2 = summ
        summ = p[0] + p0, p[1] + p1, p[2] + p2

    max_val = max(summ)
    if max_val == summ[0]:
        print("Done!\nCursive: {}%".format((summ[0] * 100) / len(prediction)))
    elif max_val == summ[1]:
        print("Done!\nSemi Square: {}%".format((summ[1] * 100) / len(prediction)))
    else:
        print("Done!\nSquare: {}%".format((summ[2] * 100) / len(prediction)))
    # shutil.rmtree(os.path.join("patches", folderID))
    # shutil.rmtree(os.path.join("raw_images", folderID))

# python main.py --predict <MODEL> <path_to_image>

run_predict("main")
