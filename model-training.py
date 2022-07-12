import cv2
import numpy as np
import tensorflow as tf

# Loading dataset
with open("dataset/labels.txt", "r") as f:
    data = np.array([x.strip().split(" ") for x in f.readlines()])

with open("dataset/out-labels.txt", "r") as f:
    labels = {}
    dt = np.array([x.strip().split(" ") for x in f.readlines()])
    for d in dt:
        labels[d[0]] = int(d[1])

nData = len(data)
print(">> Loaded dataset of length:", nData)

nTrain = int(nData * 0.7)
nTest = nData - nTrain
print(f">> Will use {nTrain} for training and {nTest} for testing")

x_train = np.array([cv2.resize(cv2.imread(x, cv2.IMREAD_GRAYSCALE), (28, 28)) for x in data[:nTrain, 0]])
y_train = np.array([labels[x] for x in data[:nTrain, 1]])
x_test = np.array([cv2.resize(cv2.imread(x, cv2.IMREAD_GRAYSCALE), (28, 28)) for x in data[nTrain:, 0]])
y_test = np.array([labels[x] for x in data[nTrain:, 1]])
print(">> Dataset successfully loaded!")

# Normalizing data
x_train = tf.keras.utils.normalize(x_train, axis=1)
x_test = tf.keras.utils.normalize(x_test, axis=1)

# Creating tensorflow model
model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Flatten(input_shape=(28, 28)))
model.add(tf.keras.layers.Dense(128, activation='relu'))
model.add(tf.keras.layers.Dense(128, activation='relu'))
model.add(tf.keras.layers.Dense(24, activation='softmax'))

# Compiling model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Training model
model.fit(x_train, y_train, epochs=25)  # Due to very small dataset epochs value is high (lower it if you have larger dataset)

# Saving model
model.save('captcha-solver.model')
