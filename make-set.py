import cv2
import numpy as np
from datetime import datetime
import time
import os

def cropAll():
    for i, file in enumerate(os.listdir("dataset/img")):
        filePath = os.path.join("dataset/imgimg", file)
        print(i, filePath)
        img = cv2.imread(filePath, cv2.IMREAD_GRAYSCALE)
        img = img[12:-12, 17:-17]
        for x in range(6):
            part = img[:, x*42:(x+1)*42]
            cv2.imwrite(f"dataset/parts/{datetime.now().timestamp()}.png", part)
            time.sleep(0.001)

            
def cropOne(name: str):
    filePath = name
    img = cv2.imread(filePath, cv2.IMREAD_GRAYSCALE)
    img = img[12:-12, 17:-17]
    for x in range(6):
        part = img[:, x*42:(x+1)*42]
        cv2.imwrite(f"test/{datetime.now().timestamp()}.png", part)
        time.sleep(0.001)


def nameAll():
    nFiles = len(os.listdir("dataset/parts"))
    f = open("dataset/labels.txt", "w")
    for i, file in enumerate(os.listdir("dataset/parts")):
        filePath = os.path.join("dataset/parts", file)
        print(f'[{i+1}/{nFiles}]={round((i+1)*100/nFiles, 1)}% - {filePath}')
        img = cv2.imread(filePath, cv2.IMREAD_GRAYSCALE)
        cv2.imshow("Image", img)
        contains = chr(cv2.waitKey(0))
        cv2.destroyAllWindows()
        print("On image is:", contains)
        f.write(f'{filePath} {contains}\n')
    f.close()


cropAll()  # Crop all images from `dataset/img`
input("Press any key to continue to manual image labeling\nYou will need to press your keyboard key corresponding to displayed image.")
nameAll()  # Name manually all parts from `dataset/parts` and store labels in `dataset/labels.txt`
