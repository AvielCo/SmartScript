import json
import logging as log
import os
from datetime import datetime

import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
from tensorflow.keras.utils import to_categorical
from tensorflow_core.python.keras.saving.save import load_model

from consts import PROJECT_DIR, MODELS_DIR, BATCH_SIZE, CLASSES
from dual_print import dual_print
from general import buildData


def main(model_type):
    filename = os.path.join(PROJECT_DIR, "logs",
                            f"{datetime.now().strftime('%d-%m-%y--%H-%M')}_evaluate-on={model_type}")
    log.basicConfig(format="%(asctime)s--%(levelname)s: %(message)s",
                    datefmt="%H:%M:%S",
                    filename=filename,
                    level=log.INFO)
    # Create model
    dual_print("Loading model...")
    try:
        model = load_model(os.path.join(MODELS_DIR, f"{model_type}.h5"))
    except IOError:
        dual_print("No model found.. exiting")
        log.shutdown()
        os.rename(filename, filename + "__DONE_WITH_ERROR.txt")
        return

    start_time = datetime.now()
    # Cache flag rom command line
    dataset, true_labels = buildData(model_type, "output_test")
    dual_print("Converting data to Numpy array")
    saved_time = datetime.now()
    dataset = np.asarray(dataset)
    dual_print("Done")
    dual_print("Reshaping Grayscale data for Conv2D dimesions")
    dataset = dataset.reshape((dataset.shape[0], dataset.shape[1], dataset.shape[2], 1))
    dual_print("Done")
    dual_print("Converting Y to categorical matrix")
    true_labels = to_categorical(true_labels)
    dual_print(f"Done")

    model_evaluation_result = model.evaluate(x=dataset, y=true_labels, batch_size=BATCH_SIZE)
    prediction_labels = model.predict(x=dataset, batch_size=BATCH_SIZE, verbose=1)

    prediction_labels = np.argmax(prediction_labels, axis=1)
    true_labels = np.argmax(true_labels, axis=1)

    # j = 0
    # # This loop saves the images that the model was calculated wrong
    # for i in range(len(true_labels)):
    #     if prediction_labels[i] != true_labels[i]:
    #         cv2.imwrite(
    #             os.path.join(os.getcwd(), "bad_patches", f"{str(j)}_true={true_labels[i]}_pred={prediction_labels[i]}.jpg"), dataset[i])
    #         j += 1

    dual_print(f"\nTested model: {model_type}\n\ttable of content:\n\t\t{json.dumps(CLASSES[model_type])}")

    conf_matrix = confusion_matrix(true_labels, prediction_labels)
    dual_print(f"\nevaluate result [loss, accuracy]: {model_evaluation_result}\n")
    dual_print(f"confusion matrix:\n{conf_matrix}\n")

    class_report = classification_report(true_labels, prediction_labels)
    dual_print(f"classification report: \n{class_report}\n")
    dual_print(f"Took: {str(datetime.now() - start_time)}")
    log.shutdown()
    os.rename(filename, filename + "__DONE.txt")
