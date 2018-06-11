"""
============================
check_imageStat.py
============================
	date: 20180116 by Jianrong Deng
        Purpose: 
           read in statistics data ( '-stat.dat' files) of an analyze period (for example data of year 2016), 
           histogram and check those data that are out of 3sigma, 5 sigma regions
        Input: 
           1: data path
           2. data date
#Note: 
#    1. data_path must be a full path, for example: 
#       data_path = /Users/jdeng/baiduCloudDisk/LAMOST/ana/outputs/run0/
#    2. examples of acceptable formats for 'date':  20160101, '2016010[1-5]'
#     please use " '2016010[1-5]' ", otherwise will get error such as:  zsh: no matches found: 2016010[1-2]
#     need to put the date in ' ', so the shell won't try to interpret
============================
"""

import statistics as sts
import fnmatch
import sys
# add 'commom' directory to python import search path
sys.path.append('../common/')
import filesIO as fIO # under ../common/ directory
import os
from os.path import join
#import pickle


#============================
def checkDistribution(data_array, Nsigma=5, info='', verbose=1):
#============================
    """
    purpose: calculate the mean pixel value and the sstd of the input image file
    input : 
       data_array: data point (in array)
       Nsigma: default is to print out points outside 5 sigma region
       info: additional info to print out 

    output: print out a list of out of range points

    """

    data = sorted(data_array)
 
    # mean and sstd of the mean array
    mean = sts.mean(data)
    sstd = sts.stdev(data)

    print( ' dataset : ', info)
    print( '    mean = ', mean, '    sstd = ', sstd)
    print ('    [  ', data[0], ' ,', data[1],  ' ,', data[2], '...,', ' ,', data[-3],  data[-2], ' ,', data[-1], ' ]')


    # check >5sigma points:
    delta_a = mean - Nsigma * sstd
    delta_b = mean + Nsigma * sstd

    print( '    check outside -', Nsigma, 'sigma points: ')
    # data point < ( mean -5sigma )
    for i in range(len(data)):
        if (data[i] < delta_a):
            if (verbose == 1): print ( '      data = ', data[i])
        else:
            np = i  # number of points outside the range
            print ( '      number of points outside the range = ', np )
            break

    print( '    check outside +', Nsigma, 'sigma points: ')
    data.sort(reverse=True)
    # data point < ( mean -5sigma )
    for i in range(len(data)):
        if (data[i] > delta_b):
            if (verbose == 1): print ( '      data = ', data[i])
        else:
            np = i  # number of points outside the range
            print ( '      number of points outside the range = ', np )
            break


    return
#============================


#============================
# main function
#============================
#
# get command line arguments and echo back
# sys.argv[0] is the script name
# sys.argv[1:] are command line arguments
print('run python script:',  sys.argv[0], sys.argv[1], sys.argv[2])

if len(sys.argv) < 3:
    print( 'Please specify data_path and data_date')
    print( 'for help, please try: python3 check_imageStat.py --help ')
    sys.exit()
 
if sys.argv[1].startswith('--'):
    option = sys.argv[1][2:]
    if option == 'usage': 
        print (' python3 check_imageStat.py data_path data_date')
    elif option == 'help':
        print ('''This program reads in stat files in data_path taken
        during the specified period (date)
             Options include:
             --usage : command line usage
             --help     : Display this help''' )
    else:
        print ('Unknow option.')

    sys.exit()

d_path = sys.argv[1]
d_date = sys.argv[2]
d_type = 'bias'
d_tag = '*stat.dat'
#file_selector = d_path + '/' + d_date + '/' + d_type
# see python3 >>> help() >>> os,  for details on fwalk
mean = []
sstd = []
medium_mean = []
medium_sstd = []
debug=True
#for root, dirs, files, rootfd in os.fwalk(d_path + '/' +d_date):
for root, dirs, files, rootfd in os.fwalk(d_path ):
   #print ( 'date: ', root)
   for ifile in sorted(files): 
      if fnmatch.fnmatch(ifile, d_tag):
         if(debug): print ( 'file: ', ifile)
         # stat file, read in stat data
         # see printStats(stats) in filesIO.py for the format of stat data 
         istat=fIO.loadStat(join(root,ifile) , debug) # get stat from ifile
         #print ('image stat where [0-4] is real data, [5] is bias medium')
         for i in range(len(istat)-1):
             mean.append(istat[i][0])
             istat_sstd = istat[i][1]
             sstd.append(istat_sstd)
             if (istat_sstd > 150): print ( ifile, ', image =', i,  ', sstd = ', istat_sstd)
         medium_mean.append(istat[5][0])  
         im_sstd = istat[5][1]
         medium_sstd.append(im_sstd)
         if (im_sstd > 150): print (ifile,  ', medium sstd = ', im_sstd)

# check distribution of the full data set points
print ('total number of points = ', len(mean))
checkDistribution(mean, 5, 'mean', 0)
checkDistribution(sstd, 5, 'sstd', 0)
print ('total number of points = ', len(medium_mean))
checkDistribution(medium_mean, 5, 'medium mean', 0)
checkDistribution(medium_sstd, 5, 'medium sstd', 0)



'''
    import glob
    file_test='/Users/jdeng/baiduCloudDisk/LAMOST/ana/outputs/run1_20171205/2016010[1-2]'
    for name in sorted(glob.glob(file_selector)):
        print(name)
        '''

