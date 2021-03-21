import shutil

import cv2
import numpy as np
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
        return
    for patch in patches_names:
        img = maintain_aspect_ratio_resize(cv2.imread(os.path.join(path, patch), 0), 224, 224)
        dataset.append(img)
    return dataset


def build_prediction_dataset(image_path: str):
    """
        This function takes an image path and creates a dataset using the patches from the image
    Args:
        image_path: image to build the dataset (patches of the image)

    Returns: dataset contains patches of the same image

    """
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
    predictions = model.predict(dataset, verbose=1)
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

    print(f"Done!\n{predicted_origin} from {predicted_shape}: {probability}%")

    shutil.rmtree(os.path.join(PROJECT_DIR, "prediction_patches", "1"))


def predict_on_shape():
    """
        Loading the main model that classify between Cursive, Semi Square and Square,
        takes an image and predicting what the shape (font) of that image.
        Then predicting the origin of the same image. (using predict_on_origin)
    """
    model = load_model(os.path.join(MODELS_DIR, "main.h5"))
    dataset = build_prediction_dataset(os.path.join(PROJECT_DIR, "predict_images", "1"))
    dataset = np.asarray(dataset)
    dataset = dataset.reshape((dataset.shape[0], dataset.shape[1], dataset.shape[2], 1))
    print("Predicting {} patches...".format(len(dataset)))
    predicted_shape, probability = extract_max_prediction(model, "main", dataset)

    print(f"Done!\n{predicted_shape}: {probability}%")
    predict_on_origin(predicted_shape, dataset)
