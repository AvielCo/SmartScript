import gc
import shutil
import sys
from datetime import datetime

import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.compat.v1 import InteractiveSession, ConfigProto
from tensorflow.keras.utils import to_categorical
from tensorflow_core.python.keras.saving.save import load_model

import crop
from callbacks import *
from consts import *
from general import buildData
from models import *

# GPU configuration
config = ConfigProto()
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)

# Const variables

# Batch size for fit function for each step in epoch
BATCH_SIZE = 128

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
print(f"Done, took: {datetime.now() - saved_time}")
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
print(f"Done, took: {str(datetime.now() - saved_time)}")
print("Calling Garbage Collector")
del y1
gc.collect()
print("Done")
print("Splitting data into train and test")
saved_time = datetime.now()
X_train, X_test, y_train, y_test = train_test_split(df, y, test_size=TEST_PERCENT, random_state=42)
inputShape = (df.shape[1], df.shape[2], df.shape[3])
print(f"Done, took: {str(datetime.now() - saved_time)}")
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

print(f"Done training.\nThe process took: {str(datetime.now() - start_time)}")
shutil.rmtree(os.path.join(crop.OUTPUT_PATH))
print(f"Done training in loop. Time took to train: {str(datetime.now() - prog_init_start_time)} ")
