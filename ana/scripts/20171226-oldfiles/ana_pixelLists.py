"""
============================
script: ana_clusters.py
============================
	date: 20170615 by Jianrong Deng
	purpose:
		generate a list of clusters from an input data file of
                above threshold pixels 
	Input: pixel lists of net data (raw - OS - bias) files
	output: cluster list
"""

import find_cluster as fcl
import filesIO as fIO
import const
import time
import os


#============================
def getPixels(pixelList):
    """
    purpose: return list of pixel ip[iy, ix]
    input: 
         pixelList, 
         with each pixel: ip[iy, ix, ivalue], 
            where [iy, ix] is pixel position, 
                  ivalue is pixel value, 
    output: 
         pixels: 
         with each pixel: ip[iy, ix]
    """
    pixels = []
    for ip in pixelList:
        pixels.append([ip[0], ip[1]])
    return pixels
#============================


#============================
def InitFlagPixels(pixelList):
    """
    purpose: return list of pixel ip[iy, ix, ivalue, iflag]
    input: 
         pixelList, 
         with each pixel: ip[iy, ix, ivalue], 
            where [iy, ix] is pixel position, 
                  ivalue is pixel value, 
    output: 
         pixels: 
         with each pixel: ip[iy, ix]
                      ivalue is pixel value, 
                      iflag set to initial value 0
    """
    pixels = []
    for ip in pixelList:
        pixels.append([ip[0], ip[1], ip[2], 0])
    return pixels
#============================



#============================
# main program
#============================


# time stamp: 
t_start = time.ctime()
t_start_clock = time.clock()
print( "Run starts. Current local time is  {} ".format(t_start))

DEBUG = const.DEBUG


# input / output filenames
#set input / output files using environment variables, create output directory if not already exist
# input file for saving pixel lists (one file for 5 lists)
file_stat = os.environ['env_filename_stat']
# mean and sstd input file (which is output from ana_image.py script)
file_pixelList = fIO.setFilename(file_stat, in_tag='stat.dat', out_tag='pixelList.dat')

file_cluster = fIO.setFilename(file_stat, in_tag='stat.dat', out_tag='clusters.dat')

if DEBUG:
    print('file_stat     :', file_stat)
    print('file_pixelList:', file_pixelList)
    print('file_clusters :', file_cluster)

# pixel lists for the >3sigma pixels
pixelLists=fIO.loadPixelLists(file_pixelList)

#read stat from previous calculation
stat = fIO.loadStat(file_stat)

clusterLists = []
for im in range(const.N_b): clusterLists.append([]) # clusterLists for the five images

# five biased images 
for im in range(const.N_b):
    if DEBUG:
        print('checking the ', im, '-th image for clusters')

    # cluster list
    clusters = []

    # pixel list of the im-th image, including pixel Value
    pV = pixelLists[im]
    # iflag set to initial value 0 for all pixels
    #pFlag = InitFlagPixels(pL)
    # list of pixel[iy, ix] positions
    ps = getPixels(pV)
    psLoop = ps.copy() # this is the list for the for looping, without popping out checked pixels
    len_psLoop = len(psLoop)
    if const.DEBUG_L2: 
        print("length of psLoop = ", len(psLoop))
        for i in range(len(psLoop)): 
            print(i, psLoop[i])

    nP = 10000
    # go through each pixel in the list
    for i in range(len(psLoop)): 
        if DEBUG:
           if i>= nP and (i/nP) - int(i/nP)==0:
                print("check the ", i, "-th pixel in the list: ", psLoop[i])
        """        
        # [index_b, index_e]: index range to look for the current pixel in the List 'ps' 
        index_b = i -  (len_psLoop - len_ps) 
        if index_b < 0: index_b = 0
        index_e = index_b + 1
        """
        len_ps = len(ps)        
        index_b = 0
        index_e = len_ps
        # list to save pixels in a cluster
        pixels = []
        # find cluster
        fcl.findCluster(ps, pV, psLoop[i],  pixels, index_b, index_e)
        if (len(pixels) > 0): 
            clusters.append(pixels)

    # get Stat
    mean = stat[im][0]
    sstd = stat[im][1]
    #if DEBUG: print ('image: ', im, 'mean=', mean, 'sstd=', sstd)

    for ic in clusters:
        pdata = []
        for ip in ic:
            # pixel value list
            pdata.append(ip[2])
        # require at least one pixel has a significantly higher number  of counts (> th_cluster)
        pdata.sort(reverse=True)
        if (pdata[0] - mean) > const.th_cluster * sstd: 
            clusterLists[im].append(ic)


# save results
# save clusterLists to file			  
# 5 lists from 5 images save in one file
if DEBUG:
    print('dump clusters to file')
fIO.dumpPixelLists(file_cluster, clusterLists)


#if DEBUG:
#    print('number of images: ', len(clusterLists))
#    for im in clusterLists:
#        print('number of clusters in a image: ', len(im))
#        for ic in im: 
#            print('number of pixels in a cluster: ', len(ic))
#            for ip in ic: 
#                print (ip[0], ip[1], int(ip[2]))


# time stamp: 
t_stop = time.ctime()
t_stop_clock = time.clock()
t_running = t_stop_clock - t_start_clock
#print( "Run starts. Current local time is  {} ".format(t_start))
print ("Run stop. Current local time is  {} ".format(t_stop))
print ("Total running time is  {} minutes".format(t_running/60 ))


