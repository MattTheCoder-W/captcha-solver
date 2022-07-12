import warnings
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
print(">> Loading libraries")

# For predicting
import cv2
import numpy as np
import tensorflow as tf

# For getting image
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import urllib.request


def cropOne(name: str):
    parts = []
    filePath = name
    img = cv2.imread(filePath, cv2.IMREAD_GRAYSCALE)
    img = img[12:-12, 17:-17]
    for x in range(6):
        parts.append(np.array(img[:, x*42:(x+1)*42]))
    return parts


def idToLabel(id: int) -> str:
    with open("dataset/out-labels.txt", "r") as f:
        labels = {}
        dt = np.array([x.strip().split(" ") for x in f.readlines()])
        for d in dt:
            labels[d[0]] = int(d[1])
        return list(labels.keys())[list(labels.values()).index(id)]
    

def waitForElement(xpath: str):
    elem = driver.find_elements(By.XPATH, xpath)
    while len(elem) == 0:
        sleep(0.1)
        elem = driver.find_elements(By.XPATH, xpath)
    return elem[0]


# Load model
print(">> Loading model")
model = tf.keras.models.load_model('captcha-solver.model')

# Create selenium webdriver
print(">> Opening Firefox")
with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    driver = webdriver.Firefox(service_log_path=os.devnull)
driver.get("https://6obcy.org/rozmowa")

rawFilePath = 'captcha.png'  # File to download
captchaImageXpath = '/html/body/div[5]/div[3]/div/div[1]/div/img'  # Captcha image xpath

# Get image url
print(">> Getting image")
imageElement = waitForElement(captchaImageXpath)
imageUrl = imageElement.get_attribute("src")

# Download image
print(">> Downloading image")
urllib.request.urlretrieve(imageUrl, rawFilePath)

# Crop downloaded image
parts = cropOne(rawFilePath)

# Predict every letter
print(">> Predicting letters in captcha")
captchaText = ""
for part in parts:
    img = np.array([cv2.resize(part, (28, 28))])
    prediction = model.predict(img)
    captchaText += str(idToLabel(np.argmax(prediction)))

print("Captcha text is:", captchaText)
