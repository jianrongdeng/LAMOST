"""
============================
test_cv2.py
============================
	date: 20180205 by Jianrong Deng
        Purpose: test the usage of cv2 moments
============================
"""

import cv2 
import numpy as np

pixels=np.zeros((2,2), dtype=int)
#pixels = [[4133, 1394, 33.3125], [4134, 1393, 18.0625]]
#pixels = [ [4133, 1394], [4134, 1393]]
np_pixels = np.zeros((2,2))
np_pixels[0, 1] = 33.3125
np_pixels[1, 0] = 18.0625
#np_pixel = ([0,33, 18, 0])
moments = cv2.moments(np_pixels)

print(moments)
