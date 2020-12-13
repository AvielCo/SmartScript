import gc
import logging as log
from datetime import datetime
from random import randint

import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from tensorflow_core.python.keras.saving.save import load_model

from callbacks import *
from consts import *
from dual_print import dual_print
from general import buildData
from models import *


def main(model_type, times):
    # # GPU configuration
    # config = ConfigProto()
    # config.gpu_options.allow_growth = True
    # session = InteractiveSession(config=config)

    prog_init_start_time = datetime.now()

    filename = os.path.join(LOG_PATH, f"{prog_init_start_time.strftime('%d-%m-%y--%H-%M')}_train_on={model_type}")
    log.basicConfig(format="%(asctime)s--%(levelname)s: %(message)s",
                    datefmt="%H:%M:%S",
                    filename=filename,
                    level=log.INFO)

    if times == 0:
        while True:
            if os.path.exists(os.path.join(PROJECT_DIR, f"output_{times}")):
                times += 1
                continue
            break

    if times == 0:
        times = 1

    # Create model
    dual_print("Loading model...")

    current_model = f"{model_type}.h5"
    if os.path.exists(os.path.join(PROJECT_DIR, "models", current_model)):
        model = load_model(current_model)
    else:
        dual_print("No model found, creating..")
        model = vgg19_architecture((224, 224, 1))
    dual_print("Done")
    model.summary(print_fn=print)

    dual_print("Creating callbacks")
    # create folders and callbacks for the fit function.
    if not os.path.exists(os.path.join(PROJECT_DIR, "checkpoints", "val_loss", model_type)):
        os.makedirs(os.path.join(PROJECT_DIR, "checkpoints", "val_loss", model_type))

    checkpoint_best = ModelCheckpoint(os.path.join(PROJECT_DIR, "models", current_model),
                                      monitor="val_accuracy",
                                      verbose=1,
                                      save_best_only=True,
                                      save_weights_only=False,
                                      mode="max", save_freq="epoch")

    callbacks = [checkpoint_best, checkpoint_val_accuracy, tensorboard]
    dual_print("Done")

    for j in range(times):
        start_time = datetime.now()

        # build data from output folder if exists. if not,
        # will crop from input_folder
        dataset, labels = buildData(model_type, f"output_{j}")

        dual_print("Converting data to Numpy array")
        # converts dataset to np array (ndarray)
        dataset = np.asarray(dataset)
        dual_print("Done")

        dual_print("Reshaping Grayscale data for Conv2D dimensions")
        # reshape dataset to fit Conv2D layers
        dataset = dataset.reshape((dataset.shape[0], dataset.shape[1], dataset.shape[2], 1))
        dual_print("Done")

        dual_print("Converting labels to categorical matrix")
        # convert labels array into matrix:
        # example:
        # classes = 3 (0, 1, 2)
        # labels = [0, 2, 1, 1, ...]
        # >>> to_categorical(labels)
        # >>> [[1, 0, 0]
        #      [0, 0, 1]
        #      [0, 1, 0]
        #      [0, 1, 0]]
        labels = to_categorical(labels)
        dual_print("Done")

        dual_print("Splitting data into train and test")
        # shuffle and split dataset and labels into train set and validation set
        seed = randint(1, 1024)  # random seed number for the shuffle of the dataset
        train_dataset, test_dataset, train_labels, test_labels = train_test_split(dataset,
                                                                                  labels,
                                                                                  test_size=TEST_PERCENT,
                                                                                  random_state=seed,
                                                                                  shuffle=True,
                                                                                  stratify=labels)
        # input_shape = (dataset.shape[1], dataset.shape[2], dataset.shape[3])

        dual_print("Done")
        dual_print("Calling Garbage Collector")
        # free memory from unneeded variables
        del labels
        del dataset
        gc.collect()
        dual_print("Done")

        dual_print("Training the model")
        # Train the model
        history = model.fit(train_dataset, train_labels,
                            validation_data=(test_dataset, test_labels),
                            epochs=EPOCHS,
                            verbose=1,
                            batch_size=BATCH_SIZE,
                            callbacks=callbacks,
                            shuffle=True)

        # val accuracy and val loss of the training
        val_accuracy = history.history['val_accuracy']
        val_loss = history.history['val_loss']

        dual_print("Training results:\n")
        i = 1
        for (v_a, v_l) in zip(val_accuracy, val_loss):
            dual_print(f"epoch {i}: val_loss: {v_l}, val_accuracy: {v_a}")
            i += 1

        dual_print(f"The process took: {str(datetime.now() - start_time)}"
                   f"\n\n\n ------------------------------------------------------------")

    dual_print(f"Done training. Time took to train: {str(datetime.now() - prog_init_start_time)} ")
    log.shutdown()
    os.rename(filename, filename + "__DONE.txt")
