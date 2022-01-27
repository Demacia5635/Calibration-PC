import threading
import time

import cv2
import numpy as np
from PyQt5.QtWidgets import QWidget

import image_process
import vars
from Utils import hsv_handler
from Utils.hsv_handler import HSV_Values

calibrate_amount: int = 0

data = []

saved_data = []


def add_info(x, y, window: QWidget):
    global calibrate_amount, saved_data
    calibrate_amount += 1

    hsv_values = hsv_handler.HSV_Values()
    thread = threading.Thread(target=hsv_from_pixel, args=(x, y, 0.5, hsv_values))
    thread.start()
    thread.join()

    saved_data = data.copy()
    for values in hsv_values.hsv:
        data.append(values)
    print(data)

    window.update_third_stream(image_process.video_image)
    update_data()


def hsv_from_pixel(x, y, values: HSV_Values):
    hsv = []
    image = cv2.cvtColor(image_process.video_image, cv2.COLOR_BGR2HSV)
    pixel = image[y, x]
    print(pixel)
    hsv.append(pixel)
    transposed_data = np.array(list(zip(*hsv))).tolist()
    h, s, v = dump_values(transposed_data[0], transposed_data[1], transposed_data[2])
    values.update(h, s, v)


def dump_values(h: list, s: list, v: list, num=1):
    h = sorted(h)[num:-num]
    s = sorted(s)[num:-num]
    v = sorted(v)[num:-num]
    return h, s, v


def add_to_calibrate(window: QWidget):
    hsv_min = []
    hsv_max = []
    min_hsv, max_hsv = image_process.get_hsv()
    if min_hsv and max_hsv:
        print(min_hsv)
        print(max_hsv)
        hsv_min.append(min_hsv)
        hsv_max.append(max_hsv)
        global calibrate_amount, saved_data
        calibrate_amount += 1

        saved_data = data.copy()
        # min:
        min_transposed_data = np.array(list(zip(*hsv_min))).tolist()
        min_h, min_s, min_v = dump_values(min_transposed_data[0], min_transposed_data[1], min_transposed_data[2], 2)
        data.append([min_h, min_s, min_v])
        # max:
        max_transposed_data = np.array(list(zip(*hsv_min))).tolist()
        max_h, max_s, max_v = dump_values(max_transposed_data[0], max_transposed_data[1], max_transposed_data[2], 2)
        data.append([max_h, max_s, max_v])

        update_data()
        window.error.setText("Added!")
        window.update_third_stream(image_process.video_image)
    else:
        window.error.setText("Cannot find; please try again!")


def update_data():
    global saved_data
    transposed_data = list(zip(*data))
    # print(transposed_data)
    if transposed_data:
        vars.lower = np.array([min(transposed_data[0]), min(transposed_data[1]), min(transposed_data[2])])
        vars.upper = np.array([max(transposed_data[0]), max(transposed_data[1]), max(transposed_data[2])])
    else:
        vars.lower = vars.lower_default
        vars.upper = vars.upper_default;
    print("lower: " + str(vars.lower))
    print("upper: " + str(vars.upper))
