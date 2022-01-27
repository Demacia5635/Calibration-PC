import cv2
import numpy as np
from cv2 import drawContours
from PyQt5.QtWidgets import QWidget

import calibration
import vars

video_image = None


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
        mask = cv2.inRange(image, vars.lower, vars.upper)
        kernal = np.ones((5, 5), np.uint8)
        # newmask = cv2.erode(mask, kernal, 2)
        newmask = cv2.dilate(mask, kernal, 2)

        contours, a = cv2.findContours(newmask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            max_radius = -1
            contour = None
            for c in contours:
                _, radius = cv2.minEnclosingCircle(c)
                if radius > max_radius:
                    max_radius = radius
                    contour = c
            if contour is not None:
                ((x, y), radius) = cv2.minEnclosingCircle(contour)
                if radius > 10 and radius <= x < oldimage.shape[1] - radius and radius <= y < oldimage.shape[0] - radius:
                    radius /= 1.15
                    pixels = []
                    pixels.append(image[int(y - radius), int(x)])
                    pixels.append(image[int(y), int(x + radius)])
                    pixels.append(image[int(y), int(x - radius)])
                    cv2.circle(oldimage, (int(x), int(y - radius)), 3, (0, 0, 0), 3)
                    cv2.circle(oldimage, (int(x), int(y - radius)), 3, (0, 0, 0), 3)
                    cv2.circle(oldimage, (int(x), int(y - radius)), 3, (0, 0, 0), 3)
                    draw = True
                    for pixel in pixels:
                        if vars.lower[0] > pixel[0] or pixel[0] > vars.upper[0] or pixel[1] <= 50:
                            draw = False
                            break
                    if draw:
                        radius *= 1.15
                        cv2.circle(oldimage, (int(x), int(y)), int(radius), (252, 40, 3), 3)
                    else:
                        radius *= 1.15
                        cv2.circle(oldimage, (int(x), int(y)), int(radius), (0, 0, 255), 3)
    return oldimage, newmask


def get_hsv():
    image = cv2.cvtColor(video_image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(image, vars.lower, vars.upper)
    kernal = np.ones((5, 5), np.uint8)
    newmask = cv2.erode(mask, kernal, 2)
    newmask = cv2.dilate(newmask, kernal, 2)

    contours, a = cv2.findContours(newmask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    min_hsv = [300, 300, 300]
    max_hsv = [-1, -1, -1]
    if len(contours) == 0:
        return None, None
    max_area = -1
    contour = None
    for c in contours:
        area = cv2.contourArea(c)
        if area > max_area:
            max_area = area
            contour = c

    M = cv2.moments(contour)
    center = [M['m10'] / M['m00'], M['m01'] / M['m00']]
    newContour = []

    for row in contour:
        vec = row[0][0] - center[0]
        vec = row[0][1] - center[1]
        vec[0] = vec[0] * vars.increase
        vec[1] = vec[1] * vars.increase

        newContour.append([vec])

    mask = np.zeros_like(mask)
    drawContours(mask, [newContour], 0, 1, -1)

    for i in range(0, image.shape[0]):
        for j in range(0, image.shape[1]):
            if mask[i][j] == 0:
                continue
            pixel = image[i][j]
            if vars.lower[0] - vars.h_max_diff <= pixel[0] <= vars.upper[0] + vars.h_max_diff:
                    if vars.lower[1] - vars.s_max_diff <= pixel[1] <= vars.upper[1] + vars.s_max_diff:
                        if vars.lower[2] - vars.v_max_diff <= pixel[2] <= vars.upper[2] + vars.v_max_diff:
                            min_hsv[0] = min(min_hsv[0], pixel[0])
                            min_hsv[1] = min(min_hsv[1], pixel[1])
                            min_hsv[2] = min(min_hsv[2], pixel[2])
                            max_hsv[0] = max(max_hsv[0], pixel[0])
                            max_hsv[1] = max(max_hsv[1], pixel[1])
                            max_hsv[2] = max(max_hsv[2], pixel[2])
    return min_hsv, max_hsv
