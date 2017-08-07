"""
=======================================
Purpose: make a histogram of the overscan region of a fits image
=======================================
Input: fits image file
Output: histogram of pixel values of the overscan region


-------------------
*By: Jianrong Deng 20170601
-------------------

"""

import numpy as np

##############################################################################
# Set up matplotlib and use a nicer set of plot parameters
import matplotlib.pyplot as plt
#from astropy.visualization import astropy_mpl_style
#plt.style.use(astropy_mpl_style)

# read in fits data file
from astropy.io import fits

image_file = '/Users/jdeng/baiduCloudDisk/LAMOST/data/20150923/bias/rb-16r-20150923235754-10000-82496157.fit.gz'

##############################################################################
# Use `astropy.io.fits.info()` to display the structure of the file:

fits.info(image_file)

##############################################################################
# Generally the image information is located in the Primary HDU, also known
# as extension 0. Here, we use `astropy.io.fits.getdata()` to read the image
# data from this first extension using the keyword argument ``ext=0``:
image_data = fits.getdata(image_file, ext=0)

##############################################################################
# The data is now stored as a 2D numpy array. Print the dimensions using the
# shape attribute:

print(image_data.shape)

# note1: overscan starts from bin x = 4096 to 4160-1 = 32 + 32 bins
# note2: the ":" takes all elements in y axis
# note3: python puts the inner most index(x) in the last
overscan = image_data[:, 4096:] 


##############################################################################
# plot the histogram
plt.figure()
plt.hist(overscan.flatten(), bins=100, range=[2150, 2250])
#plt.hist(overscan.flatten(), bins=400, range=[2100, 2500])
#plt.colorbar()
#plt.xscale('log')
#plt.yscale('log')

plt.show()


