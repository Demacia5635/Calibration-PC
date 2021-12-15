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


def hsv_from_pixel(x, y, seconds, values: HSV_Values):
    hsv = []
    start_time = time.time()
    while (time.time() - start_time) < seconds:
        image = cv2.cvtColor(image_process.video_image, cv2.COLOR_BGR2HSV)
        pixel = image[y, x]
        print(pixel)
        hsv.append(pixel)
        time.sleep(0.1)
    transposed_data = np.array(list(zip(*hsv))).tolist()
    h, s, v = dump_max_min_values(transposed_data[0], transposed_data[1], transposed_data[2])
    values.update(h, s, v)


def dump_max_min_values(h: list, s: list, v: list):
    h.sort()
    h = h[1:-1]
    s.sort()
    s = s[1:-1]
    v.sort()
    v = v[1:-1]
    return h, s, v


def add_info(x, y, window: QWidget):
    global calibrate_amount
    calibrate_amount += 1

    hsv_values = hsv_handler.HSV_Values()
    thread = threading.Thread(target=hsv_from_pixel, args=(x, y, 0.5, hsv_values))
    thread.start()
    thread.join()

    for values in hsv_values.hsv:
        data.append(values)
    print(data)

    window.update_third_stream(image_process.video_image)
    if calibrate_amount >= 3:
        update_data()


def add_to_calibrate(window: QWidget):
    min_hsv, max_hsv = image_process.get_hsv()
    if min_hsv and max_hsv:
        global calibrate_amount
        calibrate_amount += 1
        print(min_hsv)
        print(max_hsv)
        data.append(min_hsv)
        data.append(max_hsv)
        update_data()
        window.update_third_stream(image_process.video_image)
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
