# captcha-solver
Simple captcha solver in python (tensorflow)


## Requirements
* Python 3
* Required pip libraries (`requirements.txt`)
* Compiled tensorflow model (`captcha-solver.model` by default)
* If using `break-captcha-selenium.py`
    * Selenium (already in `requirements.txt`)
* Else
    * Downloaded captcha file


### To install required packages run
```bash
$ pip install -r requirements.txt 
```


## Usage
You have two options of using trained model:
* You can use selenium to open automated browser, download captcha and solve it automatically
    * `$ python break-captcha-selenium.py`
* You can break downloaded captcha image
    * `$ python break-captcha.py [-h] [-q] captcha-image`
    * Use `-h` for more informations


## Training you own model
If you want to create your own model you will need a dataset.

### Creating youw own dataset
First you can check how my dataset structure looks in `dataset` catalog. Just unzip it, look around and copy the structure.

Follow these steps to generate your own dataset:
* Download full captcha-s to `dataset/img/` catalog. (Make sure they are in supported format (image above))
    * You can use my tool for automatic captcha gathering -> `get-set.py`. It uses selenium for automatic captcha image download and creates new session (opens and closes selenium firefox) when captchas are repeating, as there is only about 5-7 unique images per session.
* Run `make-set.py` script. This script will firstly crop and separate all letters on captchas from `dataset/img/` directory and after this you will need to go through manual image labeling. In labeling process you will need to press key on you keyboard corresponding with displayed captcha part. In larger databases it can be very time consuming. WARNING: For now, this script does not support progress saving, so if you quit during labeling process and start over, it will overwrite `labels.txt` file and all previous labels.
* Now you can copy `out-labels.txt` file from my dataset and if there is such a need, add more labels to it. (do not leave gaps ex. 25, 26, 29, 30)
* And you are ready to train model now!


### Training process
Simply run `model-training.py` script.


## Warning
This model is not 100% accurate and has lots of problem with `r` and `z` characters. Bigger dataset will surely fix this.