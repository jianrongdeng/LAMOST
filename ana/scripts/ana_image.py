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

#set input / output files using environment variables, create output directory if not already exist
r_onlynames = fIO.get_onlyrawfilenames()
# output file for saving pixel lists (one file for 5 lists)
file_pixelList = fIO.setOutFilename(r_onlynames[0], d_tag='pixelList') 
# mean and sstd output file
file_stat = fIO.setOutFilename(r_onlynames[0], d_tag='stat')
# filenames with pathname
rawfiles= fIO.get_rawfilenames()

if DEBUG:
    print('rawdata files :', rawfiles)
    print('file_stat     :', file_stat)
    print('file_pixelList:', file_pixelList)


# readin images
for im in range(const.N_b): # five biased images 
    data_raw = read_fits(rawfiles[im])  # read in raw data
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
# save pixelLists to file			  
# 5 lists from 5 images save in one file
fIO.dumpPixelLists(file_pixelList, pixelLists)


# time stamp: 
t_stop = time.ctime()
t_stop_clock = time.clock()
t_running = t_stop_clock - t_start_clock
print( "Run starts. Current local time is  {} ".format(t_start))
print ("Run stop. Current local time is  {} ".format(t_stop))
print ("Total running time is  {} minutes".format(t_running/60 ))
