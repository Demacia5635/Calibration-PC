import cv2
import numpy as np
from PyQt5.QtWidgets import QWidget

import calibration
import vars

video_image = None

third_image = None


def mouse_pos(event, window: QWidget, cv_img):
    image_h, image_w, _ = cv_img.shape
    x = round(event.pos().x() * (image_w / window.video_1.size().width()))
    y = round(event.pos().y() * (image_h / window.video_1.size().height()))
    # print(video_image[y, x])
    calibration.add_info(x, y, window)


def process_image(cv_img):
    global video_image
    video_image = cv_img.copy()
    oldimage = cv_img.copy()

    image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2HSV)
    newmask = None
    if image is not None:
        image = cv2.GaussianBlur(image, (9, 9), 0)
        mask = cv2.inRange(image, vars.lower, vars.upper)
        newmask = cv2.erode(mask, None, iterations=2)
        newmask = cv2.dilate(mask, None, iterations=2)
    return oldimage, newmask

def scale_vector(vector, relative_to=[0,0]):
    diff = [0,0]
    diff[0] = vector[0] - relative_to[0]
    diff[1] = vector[1] - relative_to[1]
    diff[0] = diff[0] * vars.increase
    diff[1] = diff[1] * vars.increase
    return [int(diff[0] + relative_to[0]), int(diff[1] + relative_to[1])]

def in_adding_range(pixel):
    return vars.lower[0] - vars.h_max_diff <= pixel[0] <= vars.upper[0] + vars.h_max_diff and \
        vars.lower[1] - vars.s_max_diff <= pixel[1] <= vars.upper[1] + vars.s_max_diff and \
        vars.lower[2] - vars.v_max_diff <= pixel[2] <= vars.upper[2] + vars.v_max_diff

def get_hsv():
    global third_image, video_image
    image = cv2.cvtColor(video_image, cv2.COLOR_BGR2HSV)
    image = cv2.GaussianBlur(image, (9, 9), 0)
    mask = cv2.inRange(image, vars.lower, vars.upper)
    newmask = cv2.erode(mask, None, iterations=2)
    newmask = cv2.dilate(newmask, None, iterations=2)

    contours, _ = cv2.findContours(newmask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    min_hsv = [300, 300, 300]
    max_hsv = [-1, -1, -1]
    if len(contours) == 0:
        return None, None

    contour = max(contours, key=cv2.contourArea)

    M = cv2.moments(contour)
    center = [M['m10'] / M['m00'], M['m01'] / M['m00']]
    newContour = []

    for row in contour:
        newContour.append([scale_vector(row[0], relative_to=center)])

    new_mask = np.zeros_like(mask)
    cv2.drawContours(new_mask, np.array([newContour]), 0, 255, thickness=-1)
    new_mask = cv2.bitwise_xor(new_mask, mask, mask=new_mask)

    for i in range(0, image.shape[0]):
        for j in range(0, image.shape[1]):
            if new_mask[i][j] == 0:
                continue
            pixel = image[i][j]
            if in_adding_range(pixel):
                min_hsv[0] = min(min_hsv[0], pixel[0])
                min_hsv[1] = min(min_hsv[1], pixel[1])
                min_hsv[2] = min(min_hsv[2], pixel[2])
                max_hsv[0] = max(max_hsv[0], pixel[0])
                max_hsv[1] = max(max_hsv[1], pixel[1])
                max_hsv[2] = max(max_hsv[2], pixel[2])
    third_image = new_mask
    return min_hsv, max_hsv
