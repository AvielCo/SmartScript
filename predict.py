import shutil

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
def load_patches_from_path(path: str):
    dataset = []
    try:
        patchesNames = os.listdir(path)
    except FileNotFoundError:
        return
    for patch in patchesNames:
        img = maintain_aspect_ratio_resize(cv2.imread(os.path.join(path, patch), 0), 224, 224)
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
    dataset = load_patches_from_path(os.path.join(prediction_patches_path))
    return dataset


def get_key_from_dict(dict, value):
    return list(dict.keys())[list(dict.values()).index(value)]


def extract_max_prediction(model, model_type, dataset):
    predictions = model.predict(dataset, verbose=1)
    summ = [0] * len(predictions[0])
    for prediction in predictions:
        for i in range(len(prediction)):
            summ[i] += prediction[i]
    max_val = max(summ)
    max_index = summ.index(max_val)
    probability = (max_val * 100) / len(predictions)
    predicted_class = get_key_from_dict(CLASSES[model_type], max_index)
    return predicted_class, probability


def predict_on_origin(origin_type):
    model = load_model(os.path.join(MODELS_DIR, f"{origin_type}.h5"))
    dataset = load_patches_from_path(os.path.join(PROJECT_DIR, "prediction_patches", "1"))
    dataset = np.asarray(dataset)
    dataset = dataset.reshape((dataset.shape[0], dataset.shape[1], dataset.shape[2], 1))
    predicted_origin, probability = extract_max_prediction(model, origin_type, dataset)

    print(f"Done!\n{predicted_origin}: {probability}%")

    shutil.rmtree(os.path.join(PROJECT_DIR, "prediction_patches", "1"))


def predict_on_shape():
    model = load_model(os.path.join(MODELS_DIR, "main.h5"))
    dataset = build_prediction_dataset(os.path.join(PROJECT_DIR, "predict_images", "1"))
    dataset = np.asarray(dataset)
    dataset = dataset.reshape((dataset.shape[0], dataset.shape[1], dataset.shape[2], 1))
    print("Predicting {} patches...".format(len(dataset)))
    predicted_sub_class, probability = extract_max_prediction(model, "main", dataset)

    print(f"Done!\n{predicted_sub_class}: {probability}%")
    predict_on_origin(predicted_sub_class)
