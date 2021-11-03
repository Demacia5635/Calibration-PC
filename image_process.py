from time import sleep

import cv2
import numpy as np
import vars


def process_image(cv_img):
    oldimage = cv_img.copy()

    image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(image, vars.lower, vars.upper)
    kernal = np.ones((5, 5), np.uint8)
    newmask = cv2.erode(mask, kernal, 2)
    newmask = cv2.dilate(newmask, kernal, 2)

    contours, a = cv2.findContours(newmask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        for c in contours:
            ((x, y), radius) = cv2.minEnclosingCircle(c)
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