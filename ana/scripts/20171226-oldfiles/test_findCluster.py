"""
============================
	date: 20170812 by Jianrong Deng
	purpose:
		test findCluster function using a simple 3x3 mask input file

============================
"""

import numpy as np
import const  # constants used in LAMOST image processing
#import bits   # bit manipulate function
import find_cluster as fcl
mask = np.zeros((const.N_y, const.N_x),dtype=int )    # array to save the bitmap of each pixel
mask[0,0] = 1
mask[1,1] = 1
mask[2,1] = 1
mask[3,2] = 1
mask[2,3] = 1

mask[0,3] = 1

pFlag = np.zeros((const.N_y, const.N_x),dtype=int )

clusters = []
for ix in range(const.N_x):
    for iy in range(const.N_y):
        pixels = []
        fcl.findCluster(mask, iy, ix, pFlag, pixels)
        if (len(pixels) > 0): 
            clusters.append(pixels)

for ic in clusters:
    print(ic)
