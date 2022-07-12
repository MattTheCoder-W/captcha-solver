import os
import argparse


# File Location function for argparse (detects if file exists)
def file_location(t: str) -> str:
    if not os.path.isfile(t):
        print("Error >> File not found:", t)
        exit(1)
    return t


# Create and configure Argument Parser
parser = argparse.ArgumentParser(description="Program for breaking 6obcy captcha")
parser.add_argument("captcha-image", type=file_location, help="Downloaded captcha image file")
parser.add_argument("--quiet", "-q", action="store_true", help="Print only errors and broken captcha (useful for automation)")
args = vars(parser.parse_args())
quiet = args['quiet']  # Quiet mode flag

# Set tensorflow loggin level to 3 (nothing is printed)
if quiet:
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
print(">> Loading libraries") if not quiet else None

# For predicting
import cv2
import numpy as np
import tensorflow as tf


# Function for cropping single image with specified filename
def cropOne(name: str) -> list:
    parts = []
    filePath = name
    img = cv2.imread(filePath, cv2.IMREAD_GRAYSCALE)
    img = img[12:-12, 17:-17]
    for x in range(6):
        parts.append(np.array(img[:, x*42:(x+1)*42]))
    return parts


# Function for converting model output id to human friendly label (labels are defined in `dataset/out-labels.txt`)
def idToLabel(id: int) -> str:
    with open("dataset/out-labels.txt", "r") as f:
        labels = {}
        dt = np.array([x.strip().split(" ") for x in f.readlines()])
        for d in dt:
            labels[d[0]] = int(d[1])
        return list(labels.keys())[list(labels.values()).index(id)]


# Load model
print(">> Loading model") if not quiet else None
model = tf.keras.models.load_model('captcha-solver.model')

# Load and crop image
rawFilePath = args['captcha-image']  # Captcha image file
parts = cropOne(rawFilePath)

# Predict every letter
print(">> Predicting letters in captcha") if not quiet else None
captchaText = ""
for part in parts:
    img = np.array([cv2.resize(part, (28, 28))])
    prediction = model.predict(img, verbose="0" if quiet else "auto")
    captchaText += str(idToLabel(np.argmax(prediction)))

# Print the result
print("There is high chance that captcha is:", captchaText)  if not quiet else print(captchaText)
