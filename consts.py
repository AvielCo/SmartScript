import os
from sys import platform

path_delimiter = "\\" if platform.__contains__("win") else "/"

CURSIVE = "cursive"
SEMI_SQUARE = "semi_square"
SQUARE = "square"
INPUT = "input"
OUTPUT = "output"
BUFFER = "buffer"
CHECKPOINTS = "checkpoints"
ASHKENAZI = "ashkenazi"
SEPHARDIC = "sephardic"
ITALIAN = "italian"
BYZANTINE = "byzantine"
ORIENTAL = "oriental"
YEMENITE = "yemenite"

PROJECT_DIR = os.getcwd()
INPUT_PATH = os.path.join(PROJECT_DIR, INPUT)
OUTPUT_PATH = os.path.join(PROJECT_DIR, OUTPUT)
CURSIVE_INPUT_PATH = os.path.join(INPUT_PATH, CURSIVE)
SEMI_SQUARE_INPUT_PATH = os.path.join(INPUT_PATH, SEMI_SQUARE)
SQUARE_INPUT_PATH = os.path.join(INPUT_PATH, SQUARE)
CURSIVE_OUTPUT_PATH = os.path.join(OUTPUT_PATH, CURSIVE)
SEMI_SQUARE_OUTPUT_PATH = os.path.join(OUTPUT_PATH, SEMI_SQUARE)
SQUARE_OUTPUT_PATH = os.path.join(OUTPUT_PATH, SQUARE)
BUFFER_PATH = os.path.join(PROJECT_DIR, BUFFER)
PREDICT_BUFFER_PATH = os.path.join(PROJECT_DIR, BUFFER)
BUFFER_IMG_PATH = os.path.join(BUFFER_PATH, "buffer_img.jpg")
PREDICT_BUFFER_IMG_PATH = os.path.join(PREDICT_BUFFER_PATH, "buffer_img.jpg")
PREDICT_OUTPUT_PATH = os.path.join("patches")
PREDICT_INPUT_PATH = os.path.join("raw_images")

CLASSES_VALUE_MAIN_MODEL = {CURSIVE: 0, SEMI_SQUARE: 1, SQUARE: 2}
CLASSES_VALUE_CURSIVE_MODEL = {ASHKENAZI: 0, ITALIAN: 1, SEPHARDIC: 2}
CLASSES_VALUE_SEMI_SQUARE_MODEL = {ASHKENAZI: 0, BYZANTINE: 1, ITALIAN: 2, ORIENTAL: 3, SEPHARDIC: 4, YEMENITE: 5}
CLASSES_VALUE_SQUARE_MODEL = CLASSES_VALUE_SEMI_SQUARE_MODEL

CLASSES = {"main": CLASSES_VALUE_MAIN_MODEL,
           CURSIVE: CLASSES_VALUE_CURSIVE_MODEL,
           SEMI_SQUARE: CLASSES_VALUE_SEMI_SQUARE_MODEL,
           SQUARE: CLASSES_VALUE_SQUARE_MODEL}

# Path #1 for best val_loss
CHECKPOINT_PATH_LOSS = os.path.join(PROJECT_DIR,
                                    CHECKPOINTS,
                                    "val_loss",
                                    "model.epoch={epoch:02d}-val_loss={val_loss:.2f}.h5")

# Path #2 for best val_categorical_accuracy
CHECKPOINT_PATH_CAT_ACC = os.path.join(PROJECT_DIR,
                                       "checkpoints",
                                       "val_categorical_accuracy",
                                       "model.epoch={epoch:02d}-val_cat_acc={val_categorical_accuracy:.2f}.h5")

# Path #3 for best val_categorical_accuracy
CHECKPOINT_PATH_ACC = os.path.join(PROJECT_DIR,
                                   "checkpoints",
                                   "val_accuracy",
                                   "model.epoch={epoch:02d}-val_accuracy={val_accuracy:.2f}.h5")

CHECKPOINT_PATH_BEST = os.path.join(PROJECT_DIR, "BestModel.h5")

FIT_LOG_PATH = os.path.join(PROJECT_DIR, "logs", "fit")
LOG_PATH = os.path.join(PROJECT_DIR, "logs")

PATCH_DIMENSIONS = {"x": 400, "y": 400, "xOffset": 200, "yOffset": 200}

TRAIN_PERCENT = 0.85
TEST_PERCENT = 1 - TRAIN_PERCENT
EPOCHS = 20
BATCH_SIZE = 128

models = ["main", CURSIVE, SEMI_SQUARE, SQUARE]
description = '''
                Welcome!
Choose one of the following optional arguments
'''
epilog = f'''
                Syntax helper
------------------------------------------------------------
model = one of {models}.
path = path to the model (.h5 file); example: path/to/model.h5
times = positive integer.


'''
