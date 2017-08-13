"""
============================
ana_image.py
============================
	date: 20170812 by Jianrong Deng
	purpose:
		analysis RAW image fits files, do OS and bias subtraction
		to get REAL data. From REAL data, genreate candidate
		pixel lists and hotcell list. Save both list to files
		for further cluster analysis.
============================
"""

import filesIO as fIO
import numpy as np
import const
import image
import os
from read_fits import read_fits
import time


# time stamp: 
t_start = time.ctime()
t_start_clock = time.clock()
print( "Run starts. Current local time is  {} ".format(t_start))

DEBUG = const.DEBUG

# net = raw - OS
net     = np.zeros((const.N_b, const.N_y, const.N_x))
# real = raw - OS - bias = net - bias
real    = np.zeros((const.N_b, const.N_y, const.N_x))
mean = np.zeros((const.N_b))
sstd = np.zeros((const.N_b)) 
pixelLists = []
for im in range(const.N_b): pixelLists.append([]) # pixelLists for the five images

# modify this section for different input data file
d_path_in = '/Users/jdeng/baiduCloudDisk/LAMOST/data/'
os.system('mkdir -p {}'.format(fIO.getDir())) # create output directory if not already exists
file_stat = fIO.getFilename(tag = '-stat', postfix='.txt') # mean and sstd output file
d_time = const.test_time    # data file specification: recorded time
for im in range(const.N_b): # five biased images 
    rawFile = fIO.getFilename(path=d_path_in, time=d_time[im], tag='', postfix='.fit.gz') # input data file
    file_pixelList = fIO.getFilename(time=d_time[im], tag = '-pixelList', postfix='.txt') # output files
# modify the above section for different input data files

    data_raw = read_fits(rawFile)  # read in raw data
    net[im] = image.subtract_overscan(data_raw, DEBUG=False) # subtract Overscan

# get medium    
medium = image.getBiasMedium(net)    

# loop through five images 
for im in range(const.N_b):
   # real = net - bias
   real[im] = image.getReal(net[im], medium)

stat = image.calcStats(file_stat, real, medium)

# get mask and candidate pixelList
mask = image.getMask(real, stat, pixelLists)
# get hotcell list:
hotcellList = image.getHotcellList(mask)

if len(hotcellList)> 0: # remove hotcells
    for im in range(const.N_b): # loop through five images 
        # remove hotcell from candidate list
        pixelLists[im] = image.removeHotcell(pixelLists[im], hotcellList)

# save results
# save pixelList to file			  
fIO.dumpPixelList(file_pixelList, pixelLists)


# time stamp: 
t_stop = time.ctime()
t_stop_clock = time.clock()
t_running = t_stop_clock - t_start_clock
print( "Run starts. Current local time is  {} ".format(t_start))
print ("Run stop. Current local time is  {} ".format(t_stop))
print ("Total running time is  {} minutes".format(t_running/60 ))
