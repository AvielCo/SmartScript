from math import exp

from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.python.keras.callbacks import EarlyStopping, LearningRateScheduler, TensorBoard

from consts import *

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
