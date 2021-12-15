import numpy as np


class HSV_Values:

    def __init__(self):
        pass

    def update(self, h, s, v):
        data = [h, s, v]
        self.hsv = np.array(list(zip(*data)))
