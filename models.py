from tensorflow.keras import optimizers
from tensorflow.keras.applications import VGG19
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


def vgg19_model(input_shape):
    classes = 3
    # m = Sequential([
    #     Conv2D(64, (3, 3), activation='relu', padding='same', name='block1_conv1', input_shape=input_shape),
    #     Conv2D(64, (3, 3), activation='relu', padding='same', name='block1_conv2'),
    #     MaxPooling2D((3, 3), strides=(2, 2), name='block1_pool'),
    #
    #     # Block 2
    #     Conv2D(128, (3, 3), activation='relu', padding='same', name='block2_conv1'),
    #     Conv2D(128, (3, 3), activation='relu', padding='same', name='block2_conv2'),
    #     MaxPooling2D((2, 2), strides=(2, 2), name='block2_pool'),
    #
    #     # Block 3
    #     Conv2D(256, (3, 3), activation='relu', padding='same', name='block3_conv1'),
    #     Conv2D(256, (3, 3), activation='relu', padding='same', name='block3_conv2'),
    #     MaxPooling2D((2, 2), strides=(2, 2), name='block3_pool'),
    #
    #     # Block 4
    #     Conv2D(512, (3, 3), activation='relu', padding='same', name='block4_conv1'),
    #     Conv2D(512, (3, 3), activation='relu', padding='same', name='block4_conv2'),
    #     MaxPooling2D((2, 2), strides=(2, 2), name='block4_pool'),
    #
    #     # Block 5
    #     Conv2D(512, (3, 3), activation='relu', padding='same', name='block5_conv1'),
    #     Conv2D(512, (3, 3), activation='relu', padding='same', name='block5_conv2'),
    #     MaxPooling2D((2, 2), strides=(2, 2), name='block5_pool'),
    #
    #     Flatten(name='flatten'),
    #
    #     # Fully connected layer
    #     Dense(2048, activation='relu', name='fc1'),
    #     Dense(4096, activation='relu', name='fc2'),
    #     Dense(classes, activation='softmax', name='predictions')
    #
    # ])
    m = VGG19(include_top=True, weights=None, input_tensor=None,
              input_shape=input_shape, pooling=None, classes=classes)
    m.compile(loss=categorical_crossentropy,
              optimizer=optimizers.SGD(learning_rate=0.0005),
              metrics=["accuracy"])
    return m


def default_model_architecture(input_shape):
    dropout_rate = 0.25
    m = Sequential([
        Conv2D(32, 9, padding="same", activation="relu", strides=3, input_shape=input_shape),
        BatchNormalization(),
        MaxPooling2D((4, 4)),
        Conv2D(32, 4, padding="same", activation="relu"),
        BatchNormalization(),
        MaxPooling2D((2, 2)),
        Conv2D(32, 3, padding="same", activation="relu"),
        BatchNormalization(),
        MaxPooling2D((2, 2)),
        Flatten(),
        Dense(512, activation="relu"),
        Dropout(dropout_rate),
        Dense(256, activation="relu"),
        Dropout(dropout_rate),
        Dense(64, activation="relu"),
        Dropout(dropout_rate),
        Dense(3, activation="softmax")
    ], "default")

    m.compile(loss=categorical_crossentropy,
              optimizer=optimizers.SGD(learning_rate=0.0005),
              metrics=["accuracy"])

    return m


m = vgg19_model((224, 224, 1))
m.summary(print_fn=print)
