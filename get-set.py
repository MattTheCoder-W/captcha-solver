import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import urllib.request
from datetime import datetime

print()

def waitForElement(xpath: str):
    elem = driver.find_elements(By.XPATH, xpath)
    while len(elem) == 0:
        sleep(0.1)
        elem = driver.find_elements(By.XPATH, xpath)
    return elem[0]



captchaImageXpath = '/html/body/div[5]/div[3]/div/div[1]/div/img'
newImageButtonXpath = '/html/body/div[5]/div[3]/div/div[2]/button[1]'

urls = []
i = 1
try:
    while True:
        driver = webdriver.Firefox(service_log_path=os.devnull)
        driver.get("https://6obcy.org/rozmowa")
        reps = 0
        lastUrl = ""
        while True:
            if reps > 3:
                break
            imageElement = waitForElement(captchaImageXpath)
            imageUrl = imageElement.get_attribute("src")
            if imageUrl not in urls:
                lastUrl = imageUrl
                urls.append(imageUrl)
                print(f"[{i}] Image URL: {imageUrl}")
                filename = f'captcha_{datetime.now().timestamp()}.png'
                urllib.request.urlretrieve(imageUrl, f"dataset/img/{filename}")
                i += 1
            elif imageUrl != lastUrl:
                reps += 1
            sleep(1)
            btn = waitForElement(newImageButtonXpath)
            btn.click()
        driver.quit()
except:
    with open("dataset/urls.txt", "a") as f:
        for line in urls:
            f.write(line + "\n")

driver.quit()