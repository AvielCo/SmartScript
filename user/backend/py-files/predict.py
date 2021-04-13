import shutil

import cv2
import numpy as np
import sys
import json
from dual_print import dual_print

from tensorflow.keras.models import load_model
from consts import *
from crop import process_image
from general import maintain_aspect_ratio_resize


# Get data after the PreProcessing
def load_patches_from_path(path: str):
    """
        loading patches from path into an array
    Args:
        path: path to folder that contains the patches

    Returns: ndarray dataset with patches

    """
    dataset = []
    try:
        patches_names = os.listdir(path)
    except FileNotFoundError:
        raise FileNotFoundError("Unknown error, please try again.")
    for patch in patches_names:
        img = maintain_aspect_ratio_resize(cv2.imread(os.path.join(path, patch), 0), 224, 224)
        dataset.append(img)
    return dataset


def build_prediction_dataset():
    """
        This function takes an image path and creates a dataset using the patches from the image
    Args:
        image_path: image to build the dataset (patches of the image)

    Returns: dataset contains patches of the same image

    """
    user_predict_image_path = os.path.join(PREDICT_DIR, "predict_images")
    user_predict_patches_path = os.path.join(PREDICT_DIR, "predict_patches", user_id)
    try:
        image = os.listdir(os.path.join(user_predict_image_path, user_id))[0]
    except IndexError:
        raise IndexError("Image to predict not found.")

    process_image(path=user_predict_image_path, folder_name=user_id, image_name=image)

    dataset = load_patches_from_path(user_predict_patches_path)
    return dataset


def get_key_from_dict(dict, value):
    """
        Extracts key from dict with value
    Args:
        dict: dictionary to extract the value from
        value: the value to extract with

    Returns: key with the same value
    """
    return list(dict.keys())[list(dict.values()).index(value)]


def extract_max_prediction(model, model_type, dataset):
    """
        The function takes a model, model_type and dataset and predict the output of the model using the dataset.
        If the model_type is "main" the output of the model can be either "cursive", "square" or "semi_square"
        If the model_type is "cursive", "square" or "semi_square" the output of the model can be:
            "ashkenazi", "byzantine", "yemenite", "oriental", "italian" or "sephardic"

        for every model_type the output is also an probability of the result.
    Args:
        model (type: keras.Model): The model to predict on
        model_type (type string): The model type, can be: "main", "cursive", "semi_square" or "square"
        dataset (type ndarray): Contains the patches to predict on

    Returns:
        predicted_class (type: string): Predicted class the model has predicted using the dataset
        probability (type: float): percentage of the probability that the model has predicted
    """
    predictions = model.predict(dataset, verbose=0)
    summ = [0] * len(predictions[0])  # init summ to the len of the first predict list
    for prediction in predictions:
        for i in range(len(prediction)):
            summ[i] += prediction[i]
    max_val = max(summ)
    max_index = summ.index(max_val)
    probability = (max_val * 100) / len(predictions)
    predicted_class = get_key_from_dict(CLASSES[model_type], max_index)
    return predicted_class, probability


def predict_on_origin(predicted_shape, dataset):
    """
        Loading the predicted model that classify between "ashkenazi", "byzantine", "yemenite", "oriental",
        "italian" and "sephardic"
        takes the patches from the dataset and predicting on the predicted shape model
    Args:
        predicted_shape (type: string): the predicted shape that we got from the output of the main model
                                        using the function predict_on_shape
        dataset (type ndarray): patches of the image to predict on

    """
    model = load_model(os.path.join(MODELS_DIR, f"{predicted_shape}.h5"))
    predicted_origin, probability = extract_max_prediction(model, predicted_shape, dataset)
    success = True
    print(type(predicted_origin), type(probability), type(predicted_shape), flush=True)
    dump = json.dumps({success, predicted_origin, predicted_shape, probability})
    print(dump, flush=True)
    shutil.rmtree(user_predict_patches_path)
    print(dump)
    exit(0)


def predict_on_shape():
    """
        Loading the main model that classify between Cursive, Semi Square and Square,
        takes an image and predicting what the shape (font) of that image.
        Then predicting the origin of the same image. (using predict_on_origin)
    """
    try:
        os.makedirs(MODELS_DIR)
    except FileExistsError:
        pass
    model = load_model(os.path.join(MODELS_DIR, "main.h5"))
    try:
        dataset = build_prediction_dataset()
    except Exception as e:
        try:
            shutil.rmtree(user_predict_patches_path)
        except FileNotFoundError:
            pass
        finally:
            raise Exception(e)

    dataset = np.asarray(dataset)
    dataset = dataset.reshape((dataset.shape[0], dataset.shape[1], dataset.shape[2], 1))
    dual_print("Predicting {} patches...".format(len(dataset)))
    predicted_shape, probability = extract_max_prediction(model, "main", dataset)

    dual_print(f"Done!\n{predicted_shape}: {probability}%")
    predict_on_origin(predicted_shape, dataset)

user_id = sys.argv[1]
user_predict_image_path = os.path.join(PREDICT_DIR, "predict_images", user_id)
user_predict_patches_path = os.path.join(PREDICT_DIR, "predict_patches", user_id)
try:
    os.makedirs(user_predict_image_path)
    del(user_predict_image_path)
except FileExistsError:
    pass
try:
    shutil.rmtree(user_predict_patches_path)
except FileNotFoundError:
    pass
finally:
    os.makedirs(user_predict_patches_path)

try:
    predict_on_shape()
except Exception as e:
    print(json.dumps({"success": False, "reason": str(e)}))
    