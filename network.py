import gc
import os
import shutil
import sys
from datetime import datetime
from math import exp

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
from consts import CHECKPOINT_PATH_LOSS, PROJECT_DIR, CHECKPOINT_PATH_ACC, CHECKPOINT_PATH_BEST, \
    LOG_PATH, CHECKPOINT_PATH_CAT_ACC
from general import buildData

trainPercent = 0.7
testPercent = 1 - trainPercent
# GPU configuration
config = ConfigProto()
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)

# Const variables

# Batch size for fit function for each step in epoch
BATCH_SIZE = 128


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
        Dropout(0.5),
        # 2nd Fully Connected Layer
        Dense(4096, activation='relu'),
        # Add Dropout
        Dropout(0.5),
        # 3rd Fully Connected Layer
        Dense(1000, activation='relu'),
        # Add Dropout
        Dropout(0.5),
        # Output Layer
        Dense(3, activation='softmax')
    ], 'AlexNet')
    m.compile(loss=categorical_crossentropy,
              optimizer=optimizers.SGD(learning_rate=0.0001),
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


prog_init_start_time = datetime.now()
runCrop = True
try:
    if sys.argv[1] == "True" or sys.argv[1] == "true":
        runCrop = True
except IndexError:
    pass
start_time = datetime.now()
# Cache flag from command line
df1, y1 = buildData('input', runCrop)  # True = Starting crop process
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

# Create model
print('Loading model...')
if os.path.exists(os.path.join(os.getcwd(), 'BestModel.h5')):
    model = load_model('BestModel.h5')
else:
    print('No model found, creating..')
    model = AlexNet_architecture(inputShape)

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

print("Done training.\nThe process took: {}".format(str(datetime.now() - start_time)))
shutil.rmtree(os.path.join(crop.OUTPUT_PATH))
print("Dont training in loop. Time took to train: {} ".format(str(datetime.now() - prog_init_start_time)))