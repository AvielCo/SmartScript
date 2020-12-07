import gc
import logging as log
import os
import sys
from datetime import datetime

import cv2
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
from tensorflow.keras import Model
from tensorflow.keras.utils import to_categorical
from tensorflow_core.python.keras.saving.save import load_model

from dual_print import dual_print
from general import buildData
from consts import PROJECT_DIR


def main(input_dir, model_type):
    filename = os.path.join(PROJECT_DIR, "logs",
                            f"{datetime.now().strftime('%d-%m-%y--%H-%M')}_evaluate-on={input_dir}")
    log.basicConfig(format="%(asctime)s--%(levelname)s: %(message)s",
                    datefmt="%H:%M:%S",
                    filename=filename,
                    level=log.INFO)
    # Create model
    dual_print("Loading model...")
    model = Model()
    if os.path.exists(os.path.join(os.getcwd(), "BestModel.h5")):
        model = load_model("BestModel.h5")
    else:
        dual_print("No model found.. exiting")
        sys.exit()

    start_time = datetime.now()
    # Cache flag rom command line
    df1, y1 = buildData(input_dir, "output_test")  # True = Starting crop process
    dual_print("Converting data to Numpy array")
    saved_time = datetime.now()
    df = np.asarray(df1)
    dual_print(f"Done, took: {str(datetime.now() - saved_time)}")
    dual_print("Calling Garbage Collector")
    # del df1
    gc.collect()
    dual_print("Done")
    dual_print("Reshaping Grayscale data for Conv2D dimesions")
    df = df.reshape((df.shape[0], df.shape[1], df.shape[2], 1))
    dual_print("Done")
    dual_print("Converting Y to categorical matrix")
    saved_time = datetime.now()
    y_true = to_categorical(y1)
    dual_print(f"Done, took: {str(datetime.now() - saved_time)}")
    dual_print("Calling Garbage Collector")
    gc.collect()
    dual_print("Done")

    saved_time = datetime.now()
    eva = model.evaluate(x=df, y=y_true, batch_size=128)
    Y_pred = model.predict(x=df, batch_size=128, verbose=1)

    y_pred = np.argmax(Y_pred, axis=1)
    y_true = np.argmax(y_true, axis=1)

    del Y_pred
    del y1

    j = 0
    for i in range(len(y_true)):
        if y_pred[i] != y_true[i]:
            cv2.imwrite(
                os.path.join(os.getcwd(), "bad_patches", f"{str(j)}_true={y_true[i]}_pred={y_pred[i]}.jpg"), df1[i])
            j += 1

    a = confusion_matrix(y_true, y_pred)
    dual_print(f"\nevaluate result [loss, accuracy]: {eva}\n")
    dual_print(f"confusion matrix:\n{a}\n")

    b = classification_report(y_true, y_pred, labels=[0, 1, 2])
    dual_print(f"classification report: \n{b}\n")
    dual_print(f"Took: {str(datetime.now() - start_time)}")
    log.shutdown()
    os.rename(filename, filename + "__DONE.txt")
    # shutil.rmtree(os.path.join(crop.OUTPUT_PATH))
