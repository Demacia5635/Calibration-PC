import cv2
import numpy as np
from PyQt5.QtWidgets import QLabel, QWidget

import image_process
import vars

calibrate_amount: int = 0

data = []


def add_info(x, y, window: QWidget):
    global calibrate_amount
    calibrate_amount += 1
    image = cv2.cvtColor(image_process.video_image, cv2.COLOR_BGR2HSV)
    # print(image[y][x])
    data.append(image[y][x])
    window.update_second_stream(image_process.video_image)
    if calibrate_amount >= 3:
        update_data()


def add_to_calibrate(window: QWidget):
    min_hsv, max_hsv = image_process.get_hsv()
    if min_hsv and max_hsv:
        print(min_hsv)
        print(max_hsv)
        data.append(min_hsv)
        data.append(max_hsv)
        update_data()
        window.update_second_stream(image_process.video_image)
        # window.error.setText("Added!")
    else:
        window.error.setText("Cannot find a ball, please try again!")


def update_data():
    transposed_data = list(zip(*data))
    # print(transposed_data)
    vars.lower = np.array([min(transposed_data[0]), min(transposed_data[1]), min(transposed_data[2])])
    vars.upper = np.array([max(transposed_data[0]), max(transposed_data[1]), max(transposed_data[2])])
    print("lower: " + str(vars.lower))
    print("upper: " + str(vars.upper))