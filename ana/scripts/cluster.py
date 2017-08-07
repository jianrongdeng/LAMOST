"""
============================
cluster.py
============================
	date: 20170712 by Jianrong Deng
	purpose:
		cluster class
============================
"""

"""
The Cluster class inherits from the list class: the pixel list.
It has attributes: 
    sstd: the biased sstd used in pixel above noise threshold checking
    cv.Moments: the moments up to the third order of a rasterized shape.
"""

import cv2 

class Cluster(list):
    def __init__(self, b_sstd = 10.28, pixels = []):
         list.__init__([])
         self.sstd = b_sstd
         self.extend(pixels)
         self.moments = cv2.moments(pixels)

