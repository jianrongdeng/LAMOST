"""
=======================================
Purpose: make a histogram of fits image
=======================================
Input: fits image file
Output: histogram of pixel values


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


"""
### option for 'bins' in numpy histogram:

  ‘auto’: Maximum of the ‘sturges’ and ‘fd’ estimators. Provides good all around performance.

  ‘fd’ (Freedman Diaconis Estimator): Robust (resilient to outliers) estimator that takes into account data variability and data size.

  ‘sturges’: R’s default method, only accounts for data size. Only optimal for gaussian data and underestimates number of bins for large non-gaussian datasets.

Returns
    -------
    hist : array
        The values of the histogram. See `density` and `weights` for a
        description of the possible semantics.
    bin_edges : array of dtype float
        Return the bin edges ``(length(hist)+1)``.
Ref: https://docs.scipy.org/doc/numpy/reference/generated/numpy.histogram.html#numpy.histogram
"""

# histogram our data with numpy
# 
#hist, bins = np.histogram (image_data, 'auto')

#for i in range(len(bins)-1):
#   print ( i, '\t\t:', bins[i], '\t\t: ', hist[i])


##############################################################################
# plot the histogram
plt.figure()
#plt.hist(image_data.flatten(), bins=400, range=[2100, 2500])
plt.hist(image_data.flatten(), bins=50)
#plt.colorbar()
#plt.xscale('log')
plt.yscale('log')

plt.show()


