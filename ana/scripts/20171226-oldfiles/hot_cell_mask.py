"""
============================
script: hot_cell_mask.py
============================
	date: 20170606 by Jianrong Deng
	purpose:
		generate a mask for hot cells from 5 bias and overscan subtracted data images
	Input: 5 real images (real = biased data - overscan - bias-median)
	Output: 
		hot - cell mask
"""

# module / function to read fits file
from astropy.io import fits
from read_fits import read_fits
import bits
import numpy as np
import statistics as sts
import const 

DEBUG = True

# read in 5 data files: real = raw - overscan - bias, see subtract_overscan_median.py for detail
dir_in = '/Users/jdeng/baiduCloudDisk/LAMOST/ana/outputs/20150923/bias/'
det = 'rb-16r-'
time = [
'20150923234527-10000-82496145',
'20150923234936-10000-82496149',
'20150923235345-10000-82496153',
'20150923235754-10000-82496157',
'20150924000612-10000-82496166'
]
tag = '-sub_overscan-sub_bias'
postfix_in = '.fit'

#const.N_b = len(time) # number of biased images
#const.N_x = 4096 # the last pixel (in x) before overscan bands
#const.N_y = 4136 # total number of pixels in y direction

data = np.zeros((const.N_b, const.N_y, const.N_x)) # 5 pixel images data (after overscan and bias correction )
mask = np.zeros((const.N_y, const.N_x),dtype=int )    # array to save the bitmap of each pixel
total_hits = np.zeros((const.N_b), dtype=int) # total number of above threshold pixels in each image
pixel_value = []                            # above threshold  pixel values for the const.N_b images
# read in data
for i in range(const.N_b):
    t_i = time[i]
    file_in       = dir_in  + det + t_i + tag +  postfix_in             # input real data files
    data[i] = read_fits (file_in)



# calculate mean and sstdev (sample standard deviation)
# this is over ALL FIVE images
mean = np.mean(data)
sstd = sts.stdev(data.flatten())
if DEBUG:
    print ('mean, std: ', mean, sstd)

#mean = 0.03
#sstd = 10.28

count = 0



for it in range(const.N_b):
    pv = []
    for iy in range(const.N_y):
        for ix in range(const.N_x):
            # 3 sigma check
            pvalue = data[it, iy, ix]
            if ( pvalue - mean ) > const.th_pixel * sstd:
                  mask[iy,ix] = bits.setBit(mask[iy, ix], it)  # if > 3sigma, set the it-th bit to 1
                  total_hits[it] = total_hits[it] + 1 
                  pv.append(pvalue) # above threshold pixel values used for histogram later
    # pixel values for all images
                  pixel_value.append(pvalue)
                  
                  #if DEBUG:
                     #print ('test bit = ', bits.testBit(mask[iy, ix], it))
                     #print (data[it, iy, ix], mean, 3*sstd)
                     #print (count, iy, ix, mask[iy,ix])
            # when all images are scanned, check how many times the same pixel is fired 
            if it == (const.N_b - 1):
		     # Count number of bits set
                count = bits.bitCount(mask[iy,ix])
                if (count >=2):
                   print ('pixels with number of images fired >=2: ')
                   print (count, iy, ix, mask[iy,ix])
    print ('image:', it, '\t pixel value mean and std: ', int(sts.mean(pv)), int(sts.stdev(pv)))
    
# print total hits in each image
print ('pixel value mean and std (over all images): ', int(sts.mean(pixel_value)), int(sts.stdev(pixel_value)))

print ('total number of above threshold pixels in each images: ', total_hits)


# save mask to file			  
file_mask       = dir_in  + det + time[0] + '-' + str(const.th_pixel) + 'sigma_mask' +  postfix_in             
hdu = fits.PrimaryHDU(mask)
hdu.writeto(file_mask, overwrite='True')


#########################################################
# TODO  20170712
#
# add biased mean / sstd to mask header to be used later in the cluster selection ( 3 * sstd and 5 * sstd threshold for example)
#
#########################################################


