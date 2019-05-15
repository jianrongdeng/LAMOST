"""
============================
cluster_density.py
============================
	date: 20180515 by Jianrong Deng
        Purpose: 
	   input: read in '*-clusters,dat' data files
           output: total number of clusters (per year or per analyze
	   period) for each of the 32 CCDs. 
              
============================
"""


import numpy as np
import fnmatch
import sys
# add 'commom' directory to python import search path
sys.path.append('../common/')
import filesIO as fIO # under ../common/ directory
import const
import os
from os.path import join



"""
#============================
def usage():
#============================

# get command line arguments and echo back
# sys.argv[0] is the script name
# sys.argv[1:] are command line arguments
    print('run python script:',  sys.argv[0], sys.argv[1], sys.argv[2])

    if len(sys.argv) < 3:
        print( 'Please specify data_path and data_date')
        print( 'for help, please type: python3 cluster_density.py --help ')
        sys.exit()
     
    if sys.argv[1].startswith('--'):
        option = sys.argv[1][2:]
        if option == 'usage': 
            print (' python3 cluster_density.py data_path data_date')
        elif option == 'help':
            print ('''This program reads in '-clusters.dat' files in the data_path taken
            during the specified period (data_date)
                 Options include:
                 --usage : command line usage
                 --help     : Display this help''' )
        else:
            print ('Unknow option.')

        sys.exit()

    #d_path = sys.argv[1]
    #d_date = sys.argv[2]

    return
#============================

"""

#============================
def check_CR_density_distribution(data, Nsigma=5, info='', verbose=1):
#============================
    """
    purpose: calculate the mean value and the sstd of the inputdata array 
    input : 
       data: data point (in array)
       Nsigma: default is to print out points outside 5 sigma region
       info: additional info to print out 

    output: 
       stat: the stat info return to the main function
       print out a list of out of range points

    """

    import statistics as sts

 
    # mean and sstd of the mean array
    mean = sts.mean(data)
    sstd = sts.stdev(data)

    # the stat info return to the main function
    stat = []
    stat.append(mean)
    stat.append(sstd)


    print( ' dataset : ', info)

    # check >5sigma points:
    # delta_a = mean - Nsigma * sstd
    # delta_b = mean + Nsigma * sstd

    flag = True
    print( 'index i,\t data[i] = number of clusters in the i-th CCD')
    for i in range (0, len(data)):
       #pStr = repr(data[i]).rjust(16) # right alignment
       print(  '{0:4d}'.format (i), '{0:20d}'.format( int (data[i]) ) )
       if abs(data[i] - mean ) > Nsigma * sstd: 
           print ( ' NOTE: det ' , i , ' has data outside the ',  Nsigma,  ' sigma  region, data[i] =  {:,}'.format(int(data[i]) ))  # use the comma as a thousands separator
           flag = False
    if flag: print ( ' There is no data points outside the ',  Nsigma,  ' sigma region')


    print( '    mean = {:,}'.format(int(mean)), '    sstd = {:,} '.format( int(sstd) ) )

    return stat

#============================


#============================
# main function
#============================
#

# get command line input arguments
#usage()
# use 'input' to get input data
d_path = input('Enter the path of *-clusters.dat data: ')
# d_date = input('Enter the time period of *-clusters.dat data')

# run flags:
debug=True
#debug=False
d_type = 'bias'
d_tag = '*clusters.dat'  # data file tag name

# number of clusters for each det for the full input data set
N_cluster = np.zeros((const.N_det ), dtype=int) 
# total number of *clusters.dat files checked
N_in_dat_file = np.zeros((const.N_det), dtype=int)
#N_cluster = []


# loop through 32 CCDs:
for index in range(0, const.N_det):  # 32 CCDs, index [0, 31]  = 2 * [1, 16]
#for idet in range(0, int(const.N_det/2 - 1)):
    #for irb in range (0, 2):  # 16 CCDs in blue, 16 in red
        irb = int(index / 16) # two sets of 16 CCDs
        if (irb == 0 ): 
           rb = 'r'
        else:  
           rb = 'b'
        idet = (index + 1 ) - irb * 16
        if (idet <= 9  ):  # 01r-09r, 01b-09b
           det_tag = 'rb-0'+ str(int(idet)) + rb + '*'  # for the index of 0-9, print out as 00-09
        else: 
           det_tag = 'rb-' + str(int(idet)) + rb + '*'  
        print (index,  det_tag)   
        # loop through all files under d_path
        for root, dirs, files, rootfd in os.fwalk(d_path ):
           #print ( 'date: ', root)
           for ifile in sorted(files): 
              if fnmatch.fnmatch(ifile, d_tag): # data type: clusters
                 if fnmatch.fnmatch(ifile, str(det_tag)): # det type: [01-16][r-b]
                     if(debug and idet == 0): print ( 'file: ', ifile)
                     # clusters.dat file, read in clusters data
                     clusterLists = fIO.loadPixelLists(join(root,ifile) , False, 'clusters') # get clusters from ifile
                     # fIO.printPixelLists(clusterLists, debug, 'clusters')
                     # number of clusters in .dat files
                     N_cluster[index] +=  fIO.getNumClusters(clusterLists,debug)
                     N_in_dat_file[index] +=  1 # number of input data files

# print out results to screen and/or to output files:
print ( ' total number of *clusters.dat files analyzed = ',  N_in_dat_file.sum() )
if debug:
    print ( ' det index: \t  N of input cluster.dat files analyzed')
    for it in range(len(N_in_dat_file)): 
       #print ( '\t', end='')
       print (   (int(it + 1)), ': ', int(N_in_dat_file[it])) 

# print out total number of clusters in all CCDs
print ( ' total number of clusters found in 32 CCDs = {:,}'.format( N_cluster.sum() ) )

"""
if debug:
# individual cluster counts of each CCD
    print ( ' i-det,   \t   number of clusters')
    for id in range(const.N_det):
        if id < 16: 
            rb = 'r' 
        else:    
            rb = 'b'
        #print ( '\t', end='')    
        #pStr = '{:,}'.format( int(N_cluster[id] ) ) 
        #pStr = repr(pStr).rjust(16)
        print ( '{0:4d} {0:4d} {0:18d}'.format(  id+1 , rb,  int(N_cluster[id] ) ) ) # {:,} use the comma as a thousands separator

"""

# check statistical distribution, print out outside N_sigma * sigma points
# mean = np.mean (N_cluster)
# sstd = sts.stdev(N_cluster.flatten())
N_sigma = 3
stat = check_CR_density_distribution(N_cluster, N_sigma, 'Number of clusters found in each CCD   ', 0)


# plot out the distribution

import matplotlib.pyplot as plt
#plt.semilogy(h_Ncl, '-r*')
iDet = range(1, 33)
lMean = []
lSigmaP = []
lSigmaM = []

# add the mean & 3*sigma lines to the plot:
for id in iDet:
  lMean.append(     stat[0] )
  lSigmaP.append(   stat[0] + N_sigma * stat[1] )
  lSigmaM.append(   stat[0] - N_sigma * stat[1] )

#plt.semilogy(iDet, N_cluster, 'ro')
#plt.plot(iDet, N_cluster, 'ro', iDet, lMean, '-', iDet, lSigmaP, '--', iDet, lSigmaM, '--' )
plt.semilogy(iDet, N_cluster, 'ro', iDet, lMean, '-', iDet, lSigmaP, '--', iDet, lSigmaM, '--' )
"""  
plt.line(iDet, lMean,  '-') # draw mean value with a solid line
plt.line(iDet, lSigmaP, '--') # draw mean value with a solid line
plt.line(iDet, lSigmaM, '--') # draw mean value with a solid line
"""
#plt.grid(which='major')
plt.grid(which='both')
plt.xlabel('The index of CCDs: 1-16: r, 17-32: b')

plt.ylabel('Total Number of Candidate Cluster Events Found in Each CCD')
#plt.legend('Number of Candidate Cluster Events', 'Mean','+{}*sigma'.format(N_sigma), '-{}*sigma'.format(N_sigma)  )
#str_PSigma = '+' + str(N_sigma) + '*sigma'
#str_MSigma = '-' + str(N_sigma) + '*sigma'
#plt.legend('Number of Candidate Cluster Events', 'Mean', str(str_PSigma), str(str_MSigma) )
#plt.legend('Number of Candidate Cluster Events', 'Mean', '+ N * sigma ', '- N * sigma ')
#plt.legend('abcd')

  

plt.show()



