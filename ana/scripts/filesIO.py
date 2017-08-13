"""
============================
script: filesIO.py
============================
	date: 20170615 by Jianrong Deng
	purpose:
		handle input / output files
		various data I/O functions
	Input: input dir, date, time 
"""

import const
import pickle

#==========================
def getDir (path=const.test_path_out, date=const.test_date, datatype=const.test_datatype): 
    """
    purpose: name scheme for net data (= raw - overscan - bias) file
    """
    dir =  path + date + datatype
    return dir
#==========================

#==========================
def getFilename (path=const.test_path_out, date=const.test_date, datatype=const.test_datatype, det=const.test_det, time=const.test_time[0], tag = '-sub_overscan-sub_bias', postfix = '.fit'): 
    """
    purpose: name scheme for net data (= raw - overscan - bias) file
    """
    filename =  path + date + datatype + det + time + tag + postfix
    return filename

#==========================
def getMaskFilename(path=const.test_path_out, date=const.test_date, datatype=const.test_datatype, det=const.test_det, time=const.test_time[0], tag = '-3sigma_mask', postfix = '.fit'): 
    """
    purpose: name scheme for 3sigma-mask file
    """
    filename =  path + date + datatype + det + time + tag + postfix
    return filename

#==========================
def getClusterFilename(path=const.test_path_out, date=const.test_date, datatype=const.test_datatype, det=const.test_det, time=const.test_time[0], tag = '-cluster', postfix = '.txt'): 
    """
    purpose: name scheme for 3sigma-mask file
    """
    filename =  path + date + datatype + det + time + tag + postfix
    return filename
#============================


#============================
def dumpPixelList(file_out, pixelLists, DEBUG = const.DEBUG):
#============================
    """
    purpose: save pixel Lists to output file
    input :  filename and pixellist
    """
    # save list to output file
    try:
        with open(file_out, "wb") as data:
            pickle.dump(pixelLists, data)
    except IOError as err:
        print('File error: ', + str(err))
    except pickle.pickleError as perr:
        print('picklingerror:' + str(perr))

    if DEBUG: printPixelLists(pixelLists)

    return            
#============================

#============================
def loadPixelList(file_out, DEBUG = const.DEBUG):
#============================
    """
    purpose: load pixel List from file
    input :  filename 
    output : pixellist

    """
    # save list to output file
    try:
        with open(file_out, "rb") as data:
            pixelLists  = pickle.load(data)
    except IOError as err:
        print('File error: ', + str(err))
    except pickle.pickleError as perr:
        print('picklingerror:' + str(perr))
    
    if DEBUG: printPixelLists(pixelLists)

    return pixelLists 
#============================

#============================
def printPixelLists(pixelLists, DEBUG = const.DEBUG_L2):
#============================
    """
    purpose: print candidate  pixel List 
    input :  pixelLists

    """
    print('number of images: ', len(pixelLists))
    for im in pixelLists: # loop through five images 
        print('number of candiate pixels in the image: ', len(im))
        if DEBUG:
            for ip in im:
                print (ip[0], ip[1], int(ip[2]))
    return           
#============================


#============================
def dumpStat(file_stat, stat, DEBUG = const.DEBUG_L2):
#============================
    """
    purpose: save stat info (mean and sstd ) to output file
    input :  file_stat and data stat(mean and sstd)
    """
    try:
        with open(file_stat, "wb") as data:
            pickle.dump(stat, data)
    except IOError as err:
        print('File error: ', + str(err))

    except pickle.pickleError as perr:
        print('picklingerror:' + str(perr))

    if DEBUG:
             printStats (stat)
        
    return            
#============================


#============================
def loadStat(file_stat, DEBUG = const.DEBUG):
#============================
    """
    purpose: save stat info (mean and sstd ) to output file
    input :  file_stat and data stat(mean and sstd)
    """
    try:
        with open(file_stat, "rb") as data:
            stat = pickle.load(data)
    except IOError as err:
        print('File error: ', + str(err))

    except pickle.pickleError as perr:
        print('picklingerror:' + str(perr))
        
    if DEBUG:
             printStats (stat)

    return stat           
#============================


#============================
def printStats(stats):
#============================
    """
    purpose: print stat info (mean and sstd ) 
    input :  data stat(mean and sstd)
    """
    print ('image stat where [0-4] is real data, [5] is bias medium')
    for ist in range(len(stats)):
         print ('image :', ist, 'mean =',  stats[ist][0], ', sstd =', stats[ist][1])
    return 
#============================


