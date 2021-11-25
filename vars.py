import math

import numpy as np

aov = math.radians(50)
ball_radius = 7.86 / 100  # cm

lower = np.array([20, 40, 80])
upper = np.array([30, 255, 255])

lower_default = lower
upper_default = upper


h_max_diff = 5
s_max_diff = 10
v_max_diff = 10
