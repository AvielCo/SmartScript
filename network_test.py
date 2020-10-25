import gc
import os
import sys
from datetime import datetime

import numpy as np
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
df1, y1 = buildData('input_test', False)  # True = Starting crop process
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

saved_time = datetime.now()


scores = model.evaluate(x=df,
                        y=y,
                        verbose=1,
                        batch_size=128)

print("Test score: {}%\nTook: {}".format(str(scores[1] * 100), datetime.now() - saved_time))
# shutil.rmtree(os.path.join(crop.OUTPUT_PATH))
