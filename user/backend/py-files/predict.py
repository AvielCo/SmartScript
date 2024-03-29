import shutil

import cv2
import numpy as np
import sys
import json
import random
import string
import copy
from dual_print import dual_print

from tensorflow.keras.models import load_model
from consts import *
from crop import process_image
from general import maintain_aspect_ratio_resize

def id_generator(size=40, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


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
    input_folder_name = "guests"
    output_folder_name = random_id
    images_to_predict_path = os.path.join(PREDICT_DIR, "predict-images")
    if user_id:
        input_folder_name = output_folder_name = user_id
    
    process_image(images_to_predict_path, input_folder_name, output_folder_name, image_name)

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

    prediction_probs = [0] * len(predictions[0])  # init summ to the len of the first predict list
    for prediction in predictions: # iterate on predictions to convert to 1d array of probabilities
        for i in range(len(prediction)):
            prediction_probs[i] += prediction[i]
    
    unsorted_probabilities = copy.deepcopy(prediction_probs) # save the original probabilities and the indexes
    prediction_probs.sort(reverse=True)
    
    top_results = []
    for i in range(2):
        # extracting index of the top probabilities from unsorted array
        index = unsorted_probabilities.index(prediction_probs[i])
        probability = (prediction_probs[i] * 100) / len(predictions)
        predicted_class = get_key_from_dict(CLASSES[model_type], index)
        top_results.append((predicted_class, round(probability, 2)))
    return top_results


def predict_on_origin(top_results_shape, dataset):
    """
        Loading the predicted model that classify between "ashkenazi", "byzantine", "yemenite", "oriental",
        "italian" and "sephardic"
        takes the patches from the dataset and predicting on the predicted shape model
    Args:
        predicted_shape (type: string): the predicted shape that we got from the output of the main model
                                        using the function predict_on_shape
        dataset (type ndarray): patches of the image to predict on

    """
    top_predicted_shape = top_results_shape[0][0]
    model = load_model(os.path.join(MODELS_DIR, f"{top_predicted_shape}.h5"))
    top_results_origin = extract_max_prediction(model, top_predicted_shape, dataset)
    shutil.rmtree(user_predict_patches_path)
    print(json.dumps({"success": True, "top_results_shape": top_results_shape, "top_results_origin": top_results_origin}))
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
    top_results = extract_max_prediction(model, "main", dataset)

    # dual_print(f"Done!\n{predicted_shape}: {probability}%")
    predict_on_origin(top_results, dataset)

image_name = sys.argv[1]
user_id = False
random_id = id_generator()
try:
    user_id = sys.argv[2]
    user_predict_patches_path = os.path.join(PREDICT_DIR, "predict-patches", user_id)
except IndexError:
    user_predict_patches_path = os.path.join(PREDICT_DIR, "predict-patches", random_id)
try:
    shutil.rmtree(user_predict_patches_path)
except FileNotFoundError:
    pass
finally:
    os.makedirs(user_predict_patches_path)

try:
    predict_on_shape()
except Exception as e:
    shutil.rmtree(user_predict_patches_path)
    print(json.dumps({"success": False, "reason": str(e)}))
    
