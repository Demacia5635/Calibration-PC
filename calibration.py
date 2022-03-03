import cv2
import numpy as np
from PyQt5.QtWidgets import QWidget

import image_process
import vars

data = []

backups = []


def add_info(x, y, window: QWidget):

    image = cv2.cvtColor(image_process.video_image, cv2.COLOR_BGR2HSV)
    pixel = image[y, x]
    hsv = [pixel[0], pixel[1], pixel[2]]
    data.append((hsv, hsv))

    window.update_third_stream(image_process.video_image)
    update_data(window)


def add_to_calibrate(window: QWidget):
    min_hsv, max_hsv = image_process.get_hsv()
    if (min_hsv and max_hsv) and min_hsv[0] != 300:

        data.append((min_hsv, max_hsv))

        update_data(window)
        window.error.setText("Added!")
        window.update_third_stream(image_process.third_image, True)
    else:
        window.error.setText("Cannot find; please try again!")


def update_data(window: QWidget):
    transposed_data = np.array([hsv for values in data for hsv in values]).transpose()
    if transposed_data is not None:
        vars.lower = np.array([min(transposed_data[0]), min(transposed_data[1]), min(transposed_data[2])])
        vars.upper = np.array([max(transposed_data[0]), max(transposed_data[1]), max(transposed_data[2])])
    else:
        vars.lower = vars.lower_default
        vars.upper = vars.upper_default

    window.update_sliders()

    print('--------------------------')
    print("lower: " + str(vars.lower))
    print("upper: " + str(vars.upper))
