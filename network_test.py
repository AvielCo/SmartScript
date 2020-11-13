import gc
import os
import sys
from datetime import datetime

import cv2
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
from tensorflow.keras.utils import to_categorical
from tensorflow_core.python.keras.saving.save import load_model

from general import buildData

# Create model
print('Loading model...')

if os.path.exists(os.path.join(os.getcwd(), 'BestModel.h5')):
    model = load_model('BestModel.h5')
else:
    sys.exit()

start_time = datetime.now()
# Cache flag from command line
df1, y1 = buildData('input', True)  # True = Starting crop process
print("Converting data to Numpy array")
saved_time = datetime.now()
df = np.asarray(df1)
print(f"Done, took: {str(datetime.now() - saved_time)}")
print("Calling Garbage Collector")
# del df1
gc.collect()
print("Done")
print("Reshaping Grayscale data for Conv2D dimesions")
df = df.reshape((df.shape[0], df.shape[1], df.shape[2], 1))
print("Done")
print("Converting Y to categorical matrix")
saved_time = datetime.now()
y_true = to_categorical(y1)
print(f"Done, took: {str(datetime.now() - saved_time)}")
print("Calling Garbage Collector")
del y1
gc.collect()
print("Done")

saved_time = datetime.now()

Y_pred = model.predict(x=df, batch_size=128, verbose=1)

y_pred = np.argmax(Y_pred, axis=1)
y_true = np.argmax(y_true, axis=1)

j = 0
for i in range(len(y_true)):
    if y_pred[i] != y_true[i]:
        cv2.imwrite(
            os.path.join(os.getcwd(), "bad_patches", f"{str(j)}_true={y_true[i]}_pred={y_pred[i]}.jpg", df1[i]))
        j += 1

a = confusion_matrix(y_true, y_pred)

print(a)

b = classification_report(y_true, y_pred, labels=[0, 1, 2])
print(b)
print(f"Took: {str(datetime.now() - start_time)}")
# shutil.rmtree(os.path.join(crop.OUTPUT_PATH))
