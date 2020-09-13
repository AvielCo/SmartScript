import gc
import inspect
import os
import shutil
import sys
from datetime import datetime
from math import exp

import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.compat.v1 import InteractiveSession, ConfigProto
from tensorflow.keras import optimizers
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Dropout
from tensorflow.keras.losses import categorical_crossentropy
from tensorflow.keras.metrics import categorical_accuracy
from tensorflow.keras.models import Sequential
from tensorflow.keras.utils import to_categorical
from tensorflow.python.keras.callbacks import EarlyStopping, LearningRateScheduler, TensorBoard
from tensorflow.python.keras.layers import AveragePooling2D
from tensorflow_core.python.keras.saving.save import load_model

import crop
from consts import CLASSES_VALUE, CHECKPOINT_PATH_LOSS, PROJECT_DIR, CHECKPOINT_PATH_ACC, CHECKPOINT_PATH_BEST, \
    LOG_PATH, CHECKPOINT_PATH_CAT_ACC
from general import splitDataset, progress, shuffleDataset, maintain_aspect_ratio_resize

trainPercent = 0.7
testPercent = 1 - trainPercent
# GPU configuration
config = ConfigProto()
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)

# Const variables

# Batch size for fit function for each step in epoch
BATCH_SIZE = 128


# Get data after the PreProcessing
def loadPatchesFromPath(path: str):
    """
    This function loads patches from a given path, and gives labels to the patches from the same path.

    Parameters:
    path (str): Path to folder with patches.

    Returns:
    list: The loaded patches with the labels.
    """
    dataset = []
    patches_count = 0  # For logging
    shape_type = path.split('\\')[-1]
    try:
        classes = os.listdir(path)
    except FileNotFoundError:
        crop.logging.error("[" + inspect.stack()[0][3] + "] - Output file '" + path + "' not found.")
        return
    for c in classes:
        patches = os.listdir(os.path.join(path, c))
        print("Collecting patches from {}".format(os.path.join(path, c)))
        for i, patch in enumerate(patches):
            progress(i + 1, len(patches))
            patches_count += 1
            img = maintain_aspect_ratio_resize(cv2.imread(os.path.join(path, c, patch), 0), 227, 227)
            dataset.append(tuple((img, CLASSES_VALUE[shape_type])))
    print('collected dataset: of {}'.format(shape_type))
    return dataset


def buildData(runCrop=False):
    """
    This function builds the data from the output folders.

    Parameters:
    runCrop (bool): Cache flag.

    Returns:
    tuple: a tuple where tuple[0] is a list of the data and tuple[1] is the classes of the data.
    """
    startTime = datetime.now()
    print("[" + inspect.stack()[0][3] + "] - Starting to build the data for the Neural Network.")
    if runCrop:
        crop.main()  # PreProcessing run
    try:
        outputFolders = os.listdir(crop.OUTPUT_PATH)
    except FileNotFoundError:
        crop.logging.error("[" + inspect.stack()[0][3] + "] - Output file '" + str(crop.OUTPUT_PATH) + "' not found.")
        exit(1)

    dataset = []
    for name in outputFolders:
        print("[" + inspect.stack()[0][3] + "] - Loading patches from " + name + " Folder.")
        dataset += loadPatchesFromPath(
            os.path.join(crop.OUTPUT_PATH, name))  # Append the patches list from each output folder
        print("[" + inspect.stack()[0][3] + "] - Finished loading from " + name + " Folder.")
    # Dataset is X, classes (labels) are Y
    dataset, classes = splitDataset(shuffleDataset(dataset))
    print(
        "[" + inspect.stack()[0][3] + "] - Data build ended, execution time: " + str(datetime.now() - startTime))
    return dataset, classes


def LeNet_5_architecture(input_shape):
    m = Sequential([
        Conv2D(6, kernel_size=5, strides=1, activation='tanh', input_shape=input_shape, padding='same'),  # C1
        AveragePooling2D(),  # S2
        Conv2D(16, kernel_size=5, strides=1, activation='tanh', padding='valid'),  # C3
        AveragePooling2D(),  # S4
        Flatten(),  # Flatten
        Dense(120, activation='tanh'),  # C5
        Dense(84, activation='tanh'),  # F6
        Dense(3, activation='softmax')  # Output layer
    ])
    m.compile(loss=categorical_crossentropy,
              optimizer=optimizers.Adam(lr=0.00002),
              metrics=[categorical_accuracy])
    return m


def AlexNet_architecture(input_shape):
    m = Sequential([
        Conv2D(filters=96, input_shape=input_shape, activation='relu', kernel_size=(11, 11), strides=(4, 4),
               padding='valid'),
        # Max Pooling
        MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding='valid'),
        # 2nd Convolutional Layer
        Conv2D(filters=256, kernel_size=(11, 11), activation='relu', strides=(1, 1), padding='valid'),
        # Max Pooling
        MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding='valid'),
        # 3rd Convolutional Layer
        Conv2D(filters=384, kernel_size=(3, 3), activation='relu', strides=(1, 1), padding='valid'),
        # 4th Convolutional Layer
        Conv2D(filters=384, kernel_size=(3, 3), activation='relu', strides=(1, 1), padding='valid'),
        # 5th Convolutional Layer
        Conv2D(filters=256, kernel_size=(3, 3), activation='relu', strides=(1, 1), padding='valid'),
        # Max Pooling
        MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding='valid'),
        # Passing it to a Fully Connected layer
        Flatten(),
        # 1st Fully Connected Layer
        Dense(4096, activation='relu'),
        # Add Dropout to prevent overfitting
        Dropout(0.4),
        # 2nd Fully Connected Layer
        Dense(4096, activation='relu'),
        # Add Dropout
        Dropout(0.4),
        # 3rd Fully Connected Layer
        Dense(1000, activation='relu'),
        # Add Dropout
        Dropout(0.4),
        # Output Layer
        Dense(3, activation='softmax')
    ], 'AlexNet')
    m.compile(loss=categorical_crossentropy,
              optimizer=optimizers.SGD(learning_rate=0.001),
              metrics=['accuracy'])
    return m


def default_model_architecture(input_shape):
    return Sequential([
        Conv2D(64, (3, 3), activation="sigmoid", input_shape=input_shape),
        MaxPooling2D(pool_size=(2, 2)),
        Conv2D(64, (3, 3), activation="sigmoid"),
        MaxPooling2D(pool_size=(2, 2)),
        Conv2D(64, (3, 3), activation="sigmoid"),
        MaxPooling2D(pool_size=(2, 2)),
        Conv2D(64, (3, 3), activation="relu"),
        MaxPooling2D(pool_size=(2, 2)),
        Flatten(),
        Dense(units=128, activation='relu'),
        Dense(units=128, activation='relu'),
        Dense(units=64, activation='relu'),
        Dense(units=32, activation='relu'),
        Dense(units=3, activation="softmax"),
    ])


runCrop = False
try:
    if sys.argv[1] == "True" or sys.argv[1] == "true":
        runCrop = True
except IndexError:
    pass
start_time = datetime.now()
# Cache flag from command line
df1, y1 = buildData(runCrop)  # True = Starting crop process
print("Converting data to Numpy array")
saved_time = datetime.now()
df = np.asarray(df1)
print("Done, took: {}".format(datetime.now() - saved_time))
print("Calling Garbage Collector")
del df1
gc.collect()
print("Done")
print("Reshaping Grayscale data for Conv2D dimesions")
df = df.reshape((df.shape[0], df.shape[1], df.shape[2], 1))
print("Done")
print("Converting Y to categorical matrix")
saved_time = datetime.now()
y = to_categorical(y1)
print("Done, took: {}".format(datetime.now() - saved_time))
print("Calling Garbage Collector")
del y1
gc.collect()
print("Done")
print("Splitting data into train and test")
saved_time = datetime.now()
X_train, X_test, y_train, y_test = train_test_split(df, y, test_size=testPercent, random_state=42)
inputShape = (df.shape[1], df.shape[2], df.shape[3])
print("Done, took: {}".format(datetime.now() - saved_time))
print("Calling Garbage Collector")
del y
del df
gc.collect()
print("Done")

# d = ImageDataGenerator()
#
# saved_time = datetime.now()
# train_dataset = d.flow(
#     X_train,
#     y_train,
#     batch_size=128
# )
# print('train_dataset Took: {}'.format(datetime.now() - saved_time))
#
# saved_time = datetime.now()
# test_dataset = d.flow(
#     X_test,
#     y_test,
#     batch_size=128
# )
# print('test_dataset Took: {}'.format(datetime.now() - saved_time))
#
# saved_time = datetime.now()
# del X_test, y_test, X_train, y_train
# gc.collect()
# print('delete Took: {}'.format(datetime.now() - saved_time))

# Create model
print('Loading model...')
if os.path.exists(os.path.join(os.getcwd(), 'BestModel.h5')):
    model = load_model('BestModel.h5')
else:
    print('No model found, creating..')
    model = AlexNet_architecture(inputShape)
    # print("Compiling model")
    # model.compile(loss=categorical_crossentropy,
    #              optimizer=optimizers.Adam(lr=0.00002),
    #              metrics=[categorical_accuracy])

print('Done')
# Save the best model
print("Creating callbacks")

if not os.path.exists(os.path.join(PROJECT_DIR, 'checkpoints', 'val_loss')):
    os.makedirs(os.path.join(PROJECT_DIR, 'checkpoints', 'val_loss'))

if not os.path.exists(os.path.join(PROJECT_DIR, 'checkpoints', 'val_categorical_accuracy')):
    os.makedirs(os.path.join(PROJECT_DIR, 'checkpoints', 'val_categorical_accuracy'))

if not os.path.exists(os.path.join(PROJECT_DIR, 'checkpoints', 'val_accuracy')):
    os.makedirs(os.path.join(PROJECT_DIR, 'checkpoints', 'val_accuracy'))

checkpoint_val_loss = ModelCheckpoint(CHECKPOINT_PATH_LOSS,
                                      monitor='val_loss',
                                      verbose=1,
                                      save_best_only=True,
                                      save_weights_only=False,
                                      mode='min', save_freq='epoch')

checkpoint_val_acc = ModelCheckpoint(CHECKPOINT_PATH_CAT_ACC,
                                     monitor='val_categorical_accuracy',
                                     verbose=1,
                                     save_best_only=True,
                                     save_weights_only=False,
                                     mode='max', save_freq='epoch')

checkpoint_val_accuracy = ModelCheckpoint(CHECKPOINT_PATH_ACC,
                                          monitor='val_accuracy',
                                          verbose=1,
                                          save_best_only=True,
                                          save_weights_only=False,
                                          mode='max', save_freq='epoch')

checkpoint_best = ModelCheckpoint(CHECKPOINT_PATH_BEST,
                                  monitor='val_accuracy',
                                  verbose=1,
                                  save_best_only=True,
                                  save_weights_only=False,
                                  mode='max', save_freq='epoch')

tensorboard = TensorBoard(log_dir=LOG_PATH, histogram_freq=1, write_graph=True, write_images=True)

early_stop = EarlyStopping(monitor='val_categorical_accuracy',
                           patience=3)


def schedule(epoch, lr):
    if epoch >= 5:
        new_rate = lr * exp(-0.01)
        print('Changing learning rate from {} to {}'.format(lr, new_rate))
        return new_rate
    return lr


learning_rate_scheduler = LearningRateScheduler(schedule, verbose=1)

callbacks = [checkpoint_best, checkpoint_val_accuracy, tensorboard]

model.summary(print_fn=print)
print("Running the model")

# Train the model
model.fit(X_train, y_train,
          validation_data=(X_test, y_test),
          epochs=50,
          verbose=1,
          batch_size=BATCH_SIZE,
          callbacks=callbacks)

# Take the scores
scores = model.evaluate(x=X_test, y=y_test, verbose=1)

print("Done training.\nThe process took: {}\nTest accuracy: {}".format(str(datetime.now() - start_time),
                                                                       str(scores[1] * 100)))
shutil.rmtree(os.path.join(crop.OUTPUT_PATH))
