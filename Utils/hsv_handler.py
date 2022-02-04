import numpy as np


class HSV_Values:

    def __init__(self):
        self.hsv = None

    def update(self, h, s, v):
        self.hsv = [h, s, v]
