from tensorflow.keras import optimizers
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Dropout, BatchNormalization
from tensorflow.keras.losses import categorical_crossentropy
from tensorflow.keras.metrics import categorical_accuracy
from tensorflow.keras.models import Sequential
from tensorflow.python.keras.layers import AveragePooling2D

def LeNet_5_architecture(input_shape):
    m = Sequential([
        Conv2D(6, kernel_size=5, strides=1, activation="tanh", input_shape=input_shape, padding="same"),  # C1
        AveragePooling2D(),  # S2
        Conv2D(16, kernel_size=5, strides=1, activation="tanh", padding="valid"),  # C3
        AveragePooling2D(),  # S4
        Flatten(),  # Flatten
        Dense(120, activation="tanh"),  # C5
        Dense(84, activation="tanh"),  # F6
        Dense(3, activation="softmax")  # Output layer
    ])
    m.compile(loss=categorical_crossentropy,
              optimizer=optimizers.Adam(lr=0.00002),
              metrics=[categorical_accuracy])
    return m


def AlexNet_architecture(input_shape):
    m = Sequential([
        Conv2D(filters=96, input_shape=input_shape, activation="relu", kernel_size=(11, 11), strides=(4, 4),
               padding="valid"),
        # Max Pooling
        MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding="valid"),
        # 2nd Convolutional Layer
        Conv2D(filters=256, kernel_size=(11, 11), activation="relu", strides=(1, 1), padding="valid"),
        # Max Pooling
        MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding="valid"),
        # 3rd Convolutional Layer
        Conv2D(filters=384, kernel_size=(3, 3), activation="relu", strides=(1, 1), padding="valid"),
        # 4th Convolutional Layer
        Conv2D(filters=384, kernel_size=(3, 3), activation="relu", strides=(1, 1), padding="valid"),
        # 5th Convolutional Layer
        Conv2D(filters=256, kernel_size=(3, 3), activation="relu", strides=(1, 1), padding="valid"),
        # Max Pooling
        MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding="valid"),
        # Passing it to a Fully Connected layer
        Flatten(),
        # 1st Fully Connected Layer
        Dense(4096, activation="relu"),
        # Add Dropout to prevent overfitting
        Dropout(0.5),
        # 2nd Fully Connected Layer
        Dense(4096, activation="relu"),
        # Add Dropout
        Dropout(0.5),
        Dense(3000, activation="relu"),
        Dropout(0.5),
        Dense(2000, activation="relu"),
        Dropout(0.5),
        # 3rd Fully Connected Layer
        Dense(1000, activation="relu"),
        # Add Dropout
        Dropout(0.5),
        # Output Layer
        Dense(3, activation="softmax")
    ], "AlexNet")
    m.compile(loss=categorical_crossentropy,
              optimizer=optimizers.SGD(learning_rate=0.0001),
              metrics=["accuracy"])
    return m


def default_model_architecture(input_shape):
    m = Sequential([
        Conv2D(32, (2, 2), padding="same", activation="relu", input_shape=input_shape),
        BatchNormalization(),
        MaxPooling2D((4, 4)),
        Dropout(0.3),
        Conv2D(32, (2, 2), padding="same", activation="relu"),
        BatchNormalization(),
        MaxPooling2D((2, 2)),
        Dropout(0.3),
        Conv2D(32, (2, 2), padding="same", activation="relu"),
        BatchNormalization(),
        MaxPooling2D((2, 2)),
        Dropout(0.3),
        Flatten(),
        Dense(128, activation="relu"),
        BatchNormalization(),
        Dropout(0.3),
        Dense(64, activation="relu"),
        BatchNormalization(),
        Dropout(0.3),
        Dense(3, activation="softmax")

    ], "default")

    m.compile(loss=categorical_crossentropy,
              optimizer=optimizers.Adam(learning_rate=0.0001),
              metrics=["accuracy"])

    return m

# m = default_model_architecture((227,227, 1))
# m.summary(print_fn=print)
