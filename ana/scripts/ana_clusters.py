"""
============================
script: ana_clusters.py
============================
	date: 20170615 by Jianrong Deng
	purpose:
		analyze clusters
	Input: mask file and net data (raw - OS - bias) files
	output: cluster list
"""

import find_cluster as fcl
import filesIO as fIO
import numpy as np
import statistics as sts
import const
import bits 
import image
from read_fits import read_fits


hotcell = np.zeros((const.N_y, const.N_x),dtype=int )    # array to save the bitmap of each HOTCELL 

# mask matrix for the >3sigma pixels
mask =  read_fits(fIO.getMaskFilename())
hotcellList = getHotcellList(mask)

# flag hotcells
for iy in range(const.N_y):
    for ix in range(const.N_x):
    # check if any hotcells in the 5 biased images
    count = bits.bitCount(mask[iy,ix]) # number of images with pixel ix-iy fired 
    if (count == 5):  # if pixel fired in all FIVE image, flag as hotcell
	hotcell[iy,ix] = 1  # if > 3sigma, set the it-th bit to 1
	print ('pixels with number of images fired >=5: ')
	print (count, iy, ix, hotcell[iy,ix])


# five biased images 
for im in range(const.N_b):

    # save cluster to file			  
    file_cluster = fIO.getClusterFilename(time=const.test_time[im])

    if const.DEBUG:
        print ('image: ', im)

    # cluster list
    clusters = []
    # matrix used to save flags of the pixel (if it is already checked or not)
    pFlag = np.zeros((const.N_y, const.N_x),dtype=np.int8)
    # go through each pixel
    for iy in range(const.N_y):
         for ix in range(const.N_x):
                pixels = []
                # find cluster
                fcl.findCluster(mask, hotcellList, iy, ix, pFlag, pixels, im)
                if (len(pixels) > 0): 
                    clusters.append(pixels)

    # read in pixel values (these should be values after Overscan and biased subtraction)
    data =  read_fits(fIO.getFilename(time=const.test_time[im]))
    # calculate mean and sstdev (sample standard deviation)
    mean = np.mean(data)
    sstd = sts.stdev(data.flatten())
    print ('mean=', mean, 'sstd=', sstd)

    # cluster list including pixel values
    pclusters = []
    for ic in clusters:
        pcl = []
        pdata = []
        for ip in ic:
            # cluster list
            pcl.append([ip[0], ip[1], data[ip[0],ip[1]]])
            # pixel value list
            pdata.append(data[ip[0],ip[1]])
        # require at least one pixel has a significantly higher number  of counts (> th_cluster)
        pdata.sort(reverse=True)
        if (pdata[0] - mean) > const.th_cluster * sstd: 
            pclusters.append(pcl)


    # save cluster to output file
    try:
        with open(file_cluster, "w") as data:
            #print("{}".format(pclusters), file=data)
            for ic in pclusters:
                print("[", file=data)
                for ip in ic: 
                    # if not the last element
                    if ip != ic[len(ic)-1]:
                        print ("[", ip[0], ",", ip[1], ",", int(ip[2]), "], ", file=data)
                    # if is the last element, no "," printed after "]"
                    else:    
                        print ("[", ip[0], ",", ip[1], ",", int(ip[2]), "] ", file=data)
                print("]", file=data)

    except IOError as err:
        print('File error: ', + str(err))


    if const.DEBUG:
        print('number of clusters in the image: ', len(pclusters))
        for ic in pclusters:
            print('number of pixels in a cluster: ', len(ic))
            for ip in ic: 
                print (ip[0], ip[1], int(ip[2]))

