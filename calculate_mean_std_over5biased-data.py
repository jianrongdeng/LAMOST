"""
=======================================
script: calculate_mean_std_over5biased-data.py
=======================================

*By: Jianrong Deng 20170523
Purpose: take 5 biased data image_i, calculate mean and standard deviation (std) over the 5 images
Input: 5 biased data
Output: mu, std and image_i - mu
-------------------
"""


from astropy.io import fits
import numpy as np
import statistics as st

DEBUG = 'True'

##############################################################################
# read in 5 biased files
dir_in = '/Users/jdeng/baiduCloudDisk/LAMOST/data/20150923/bias/'
dir_out = '/Users/jdeng/baiduCloudDisk/LAMOST/ana/outputs/20150923/bias/'
det = 'rb-16r-'
time = [
'20150923234527-10000-82496145',
'20150923234936-10000-82496149',
'20150923235345-10000-82496153',
'20150923235754-10000-82496157',
'20150924000612-10000-82496166'
]
postfix_in = '.fit.gz'
postfix_out = '.fit'
file_in = []
file_out = []
file_out_std = []
file_out_2std = []
file_out_3std = []
fig_out = []

# input and output file names
file_mean = dir_out + det + time[0] + '-mean' + postfix_out    # output file for the mean over all images from one det
file_std = dir_out + det + time[0] + '-std' + postfix_out   # output file for the standard deviation
for t_i in time:
   file_in.append(dir_in + det + t_i + postfix_in)             # input biased data files
   file_out.append(dir_out + det + t_i +'-sub_mean' + postfix_out)  # output images with mean subtracted
   file_out_std.append(dir_out + det + t_i +'-sub_mean-sub_std' + postfix_out) # output images = input - mean - std
   file_out_2std.append(dir_out + det + t_i +'-sub_mean-sub_2std' + postfix_out) # output images = input - mean - 2std
   file_out_3std.append(dir_out + det + t_i +'-sub_mean-sub_3std' + postfix_out) # output images = input - mean - 3std
   fig_out.append(dir_out + 'figures/' + det + t_i +'-overscan-mean-sstd-x-y.png')  # output images with mean subtracted

if DEBUG:
   for i in file_in:
     print (i)
   for i in file_out:
     print (i)
   for i in file_out_3std:
     print (i)
   print (file_mean)  
   print (file_std)

# read in fits data   
images = []
for i in file_in:
   images.append (fits.getdata(i, ext=0))
   

# calculate mean and std deviation, that is average over 5 images
mean = np.mean(images, axis = 0)  # along x-axis, which will calculate the mean of the images

# create a new fits file with image data = mean
hdu_mean = fits.PrimaryHDU(mean)
hdu_mean.writeto(file_mean, overwrite='True')

# for std, see reference: 
#   https://docs.python.org/3.4/library/statistics.html
#   https://docs.scipy.org/doc/numpy/reference/generated/numpy.std.html#numpy.std
# calculate standard deviation along x-axis, which is over 5 images
std = np.std(images, axis = 0)
# create a new fits file with image data = std
hdu_std = fits.PrimaryHDU(std)
hdu_std.writeto(file_std, overwrite='True')

# for each image, do: image_out = image_in - mean
N_images = len(images)  # total number of images
for i in range(N_images):
   net = images[i] - mean
   hdu_out = fits.PrimaryHDU(net)
   hdu_out.writeto(file_out[i], overwrite='True')
   # image_std = input - mean -  std
   net_sub_std = net -  std
   hdu_out_std = fits.PrimaryHDU(net_sub_std)
   hdu_out_std.writeto(file_out_std[i], overwrite='True')
   # image_2std = input - mean - 2 * std
   net_sub_2std = net - 2 * std
   hdu_out_2std = fits.PrimaryHDU(net_sub_2std)
   hdu_out_2std.writeto(file_out_2std[i], overwrite='True')
   # image_3std = input - mean - 3 * std
   net_sub_3std = net - 3 * std
   hdu_out_3std = fits.PrimaryHDU(net_sub_3std)
   hdu_out_3std.writeto(file_out_3std[i], overwrite='True')

