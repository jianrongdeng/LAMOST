"""
============================
image.py
============================
	date: 20170810 by Jianrong Deng
	purpose:
		image class
============================
"""
import bits
import const
import numpy as np
import statistics as sts
from astropy.io import fits
import os
import filesIO as fIO

#============================
def imageStats(imagefile, DEBUG = 1):
#============================
    """
    purpose: calculate the mean pixel value and the sstd of the input image file
    input : image filename
    output: stat (mean and sstd) value 
    """


    data = fits.getdata(imagefile)

    return imageDataStats(data) 
#============================

#============================
def imageDataStats(data, DEBUG = 1):
#============================
    """
    purpose: calculate the mean pixel value and the sstd of the input image
    input : image matrix
    output: mean and sstd value 
    """

    # calculate mean and sstdev (sample standard deviation)
    mean = np.mean(data)

    sstd = sts.stdev(data.flatten())
    if DEBUG: 
         print ('mean=', mean, 'sstd=', sstd)

    stat = []
    stat.append(mean)
    stat.append(sstd)

    return  stat
#============================

#============================
def calcStats(file_stat, real, medium, DEBUG = 1):
#============================
    """
    purpose: get stat info for the real and medium matrix
    input : 
         file_stat: filename where stat info is saved
         real: 5 image matrix with real data
         medium: bias medium matrix
    output: stat info
    """
    stat = []
    # get stat of each image
    if os.system('ls -l {}'.format( file_stat)) == 0 and DEBUG: # if file_stat exists
       # in DEBUG mode:  read stat from previous calculation (if exists) to save time
       stat = fIO.loadStat(file_stat)
    else:    
       for im in range(const.N_b):
          # calculate statistics of real data on the spot
          stat.append(imageDataStats(real[im]))

       stat.append(imageDataStats(medium)) # stat of bias medium matrix
       # save stat info (mean and sstd) to file    
       fIO.dumpStat(file_stat, stat, DEBUG=DEBUG)

    return stat
#============================



#============================
def subtract_overscan(raw, DEBUG = 1):
#============================
    """
    purpose: overscan subtraction
    input : raw image matrix
    output: net = raw - OS 
    """
    

    os_x_min = []
    os_x_max = []
    data_x_min = [] # define two amplifier regions in data
    data_x_max = []
    os_mean = np.zeros((const.N_y,const.N_os))
    #os_sstd = np.zeros((const.N_y,const.N_os)) 
    os_pstd = np.zeros((const.N_y,const.N_os)) 
    overscan= np.zeros((const.N_y,const.N_x))
    net     = np.zeros((const.N_y,const.N_x))
    for i in range(const.N_os):   # loop through N_os overscan regions
            # [4096, 4096 + 32], [4096 + 32, 4096 + 32 + 32]
            # note: in python, an array with index [a, b], a will be inclusive, b will be exclusive
            os_x_min.append(const.N_x  + i * const.OS_Nbins )
            os_x_max.append( os_x_min[i] + const.OS_Nbins )
            # region 1: x = [0 : N_x/N_os]
            # region 2: x = [N_x/N_os : N_x]
            data_x_min.append(int(i * const.N_x/const.N_os) )
            data_x_max.append(int(data_x_min[i] + const.N_x/const.N_os) )
            for j_y in range(const.N_y): # loop through pixels along the y axis
	    # the sub-array of the overscan region
                    os_data =  (raw[j_y, os_x_min[i]:os_x_max[i] ] )  # note: the first index is y-axis, the second axis is x
                    # calculate mean and std deviation using values in the overscan region
                    # average over OS_Nbins (=32, along x-axis)
                    os_mean[j_y, i] =  np.mean(os_data)   #  calculate the mean for the two overscan regions
                    # sample standard deviation
                    # os_sstd[j_y, i] =  (sts.stdev(os_data.flatten()))
                    # population standard deviation
                    os_pstd[j_y, i] = (np.std(os_data))
                    # subtract overscan
                    overscan[j_y, data_x_min[i]:data_x_max[i]] =  os_mean[j_y, i] # use mean value along x-axis for OS subtraction
                    net[j_y, data_x_min[i]:data_x_max[i]] = raw[j_y, data_x_min[i]:data_x_max[i] ] - os_mean[j_y, i]
    
                    if DEBUG :
                       if j_y < 5:
                          #print (i, j_y, os_x_min[i], os_x_max[i], 'os mean = ',  os_mean[j_y, i],'\t', 'os sstd:', os_sstd[j_y, i], '\t', 'os_pstd: ', os_pstd[j_y, i])
                          print ('os region =', i, 'y = ',  j_y, ', x = [',  os_x_min[i], os_x_max[i], '], os mean = ',  os_mean[j_y, i],'\t', 'os_pstd: ', os_pstd[j_y, i])
                          print ('raw data: ', raw[j_y, data_x_min[i]:data_x_min[i] + 5 ])
                          print ('net = raw - os :' , net[j_y, data_x_min[i]:data_x_min[i] + 5])
    return net
#============================


#============================
def getBiasMedium(net, DEBUG = const.DEBUG):
    """
    purpose: take bias files and return the medium value 
    input : net image matrix
    output: medium = medium (bias)
    """
    # find the median from net[0-5] = image[0-5] - OS

    # note: net     = np.zeros((const.N_b, const.N_y,const.N_x))
    medium = np.median(net, axis = 0) #  along the first axis, which will be over the N_b images
    """
    if DEBUG:
       print('medium image: ')
       imageDataStats(medium) # check stat
    """

    return medium
#============================

#============================
def getReal( net, medium): 
#============================
    """
    purpose: subtract bias from input data
    input : net (= raw - overscan) image matrix
    output: real = net - bias-medium
    """
    real = net - medium

    return real
#============================

#============================
def getMask(data, stat, pixelLists, DEBUG=const.DEBUG):
#============================
    """
    purpose: generate mask matrix to mark pixels above threshold
    input : real(= raw - overscan -bias) image matrix
            note:   real data = data[i] = read_fits (file_in[i])
            stat: stat[i] = [mean[i], sstd[i]]
                mean = mean[i]
                sstd = sstd[i], where i is the ith image
    output: mask matrix where > threshold pixels are marked
            pixelLists: pixel[i], list of candidate pixels of the ith image
    """

    mask = np.zeros((const.N_y, const.N_x),dtype=int )    # array to save the bitmap of each pixel
    for it in range(const.N_b):
        mean = stat[it][0]
        sstd = stat[it][1]
        for iy in range(const.N_y):
            for ix in range(const.N_x):
                # 3 sigma check
                pvalue = data[it, iy, ix]
                if ( pvalue - mean ) > const.th_pixel * sstd:
                      mask[iy,ix] = bits.setBit(mask[iy, ix], it)  # if > 3sigma, set the it-th bit to 1
                      pixelLists[it].append([iy, ix, pvalue])
        if DEBUG:
            print('image ', it, ' has ', len(pixelLists[it]), ' candidate pixels')
    return mask
#============================

#============================
def getHotcell(mask, DEBUG=const.DEBUG):
#============================
    """
    purpose: generate mask matrix to mark pixels above threshold
    input: mask matrix where > threshold pixels are marked
    output: hotcell matrix, hotcell map of the current CCD chip
    """

    hotcell= np.zeros((const.N_y, const.N_x),dtype=int )    # array to save the hotcell map of the chip
    for iy in range(const.N_y):
        for ix in range(const.N_x):
             if isHotcell(mask, iy, ix):
                 hotcell[iy, ix] = 1
    if DEBUG:
        print('total number of hot cell= ', hotcell.sum())
    return hotcell
#============================

#============================
def isHotcell(mask, iy, ix, N_image=const.N_b, DEBUG=const.DEBUG):
    """
    purpose: check if pixel iy-ix is a hotcell
    input: mask matrix where > threshold pixels are marked
           iy, ix: pixel position
           N_image: number of images used to check hotcells
    output: hotcell matrix, hotcell map of the current CCD chip
    """
    flag = False 
    count = bits.bitCount(mask[iy,ix])
    if count == N_image: # if the pixel fired in all images, mark it as a hotcell
        flag = True
        if DEBUG: 
            print('hot cell, iy = ', iy, ', ix =', ix)
    return flag
#============================

#============================
def getHotcellList(mask, N_image=const.N_b, DEBUG=const.DEBUG):
#============================
    """
    purpose: generate hotcell list
    input: mask matrix where > threshold pixels are marked
           N_image: number of images used to check hotcells
    output: hotcell list of the current CCD chip
    """
    hotcellList = []
    for iy in range(const.N_y):
        for ix in range(const.N_x):
             if isHotcell(mask, iy, ix):
                 hotcellList.append([iy, ix])
    if DEBUG:
        print('total number of hot cell= ', len(hotcellList))
    return hotcellList
#============================

#============================
def inHotcellList(hotcellList, iy, ix):
#============================
    """
    purpose: check if pixel iy-ix in the hotcellList
    input: hotcellList, pixel position iy-ix
    output: return True if it is hotcell
    """
    if [iy, ix] in hotcellList: return True
    return False
#============================

#============================
def isCandidatePixel(pixelList, iy, ix):
    """
    purpose: check if pixel iy-ix is a candidate pixel
    input: candidate pixel list
           iy, ix: pixel position
    output: true if it is an above threshold pixel
    """
    flag = False 
    for ip in pixelList:
         if ip[0] == iy: 
             if ip[1] == ix:
                 return True
    return flag
#============================

#============================
def removeHotcell(pixelList, hotcellList, DEBUG= const.DEBUG):
#============================
    """
    purpose: remvoe hotcells from candidate pixel list
    input: hotcellList, pixel candidate list
    output: list of good candidate pixels
    """
    for ip in pixelList:
        if [ip[0], ip[1]] in hotcellList: 
            pixelList.remove(ip)
    if DEBUG:
        print('there are ', len(pixelList), ' candidate pixels after hotcell removing')
    return pixelList
#============================


