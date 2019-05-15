"""
============================
cluster_hist.py
============================
	date: 20180529 by Jianrong Deng
        Purpose: 
	   Plot out various histograms of clusters' distributions
	   input: clusterList
           output: histograms 
============================
"""
import matplotlib.pyplot as plt
import numpy as np
import os
from os.path import join
import fnmatch
import sys
# add 'commom' directory to python import search path
sys.path.append('../common/')
import const
import filesIO as fIO # under ../common/ directory


#============================
def list2hist1d (clusterLists, debug = True) : 
#def list2hist1d (clusterLists) : 
#============================
    """
    purpose: histogram distribution information in an input cluster list 
    input : 
       clusterLists: a list of clusters 
       debug: debugging flag
    output: distribution histograms

    """
   
    # the maximum number of pixels in a cluster = const.N_x * const.N_y
    N_cl      = np.zeros( ( const.N_x * const.N_y ), dtype=int) 
    Np_max = 0  # the maximum number of pixels in a cluster
    # get the number of cluster of Np (number of pixel)
    for ic in clusterLists: 
       Np = len(ic)
       if Np > Np_max: Np_max = Np
       N_cl     [Np] += 1

    # plot of the distribution   
    # the array used in plotting 
    x     = np.zeros( ( Np_max + 1), dtype = int)       
    h_Ncl = np.zeros( ( Np_max + 1), dtype = int)
    for i in range(1, Np_max + 1 ): 
       x[i] = i
       h_Ncl[i] = N_cl[i]
    if debug: 
      for i in range(Np_max+1): print (x[i] , '\t', N_cl[i], '\t', h_Ncl[i])

      print (x[1], h_Ncl[1], '\t', x[-1], h_Ncl[-1] ) # print out the N_p = 1 bin, and the N_p max bin


    #plt.plot(x, N_cl, 'r*-')
    plt.semilogy(h_Ncl, '-r*')
    plt.show()


    return
#============================

#============================
# main function
#============================
#

debug = True
#debug = False

d_tag = '*clusters.dat'  # data file tag name

# get the running mode
mode = input('Enter "1" for one file mode, "2" for multiple files mode:') 

if mode == '1': 

    # use 'input' to get the input data filename
    d_file = input('Enter the name of the *-clusters.dat file to be checked: ')

    # clusters.dat file, read in clusters data
    clusterLists = fIO.loadPixelLists( d_file , False, 'clusters') # get clusters from the input data file

    N_cluster = 0
    m = 0
    # check the first five clusters ( one cluster in each image)
    for im in clusterLists: # loop through five images 
           N_im = len(im)
           N_cluster += N_im
           m +=1
           print (' number of clusters in the {}-th image = {}'.format(m, N_im ) )
           #for icluster in im: # loop through the clusters
           list2hist1d( im, debug)

    print (' total number of clusters in the input file = ', int(N_cluster) )

elif mode == '2':
    # use 'input' to get the path of the input data files, and the CCD name
    d_path = input('Enter the path of the *-clusters.dat files to be checked: ')
    #det_tag = '*01r*'
    det_tag = input('Enter the CCD name tag of the *-clusters.dat files to be checked: (ex: 01b, 01r) ')
    det_tag = '*' + det_tag + '*'

    if debug:
       print ('d_path = {}, det_tag = {}'.format(d_path, det_tag))
       print('det_tag = {}, str(det_tag) = {}, repr(det_tag) = {}'.format(  det_tag, str(det_tag), repr(det_tag)))


    # the maximum number of pixels in a cluster = const.N_x * const.N_y
    N_cl      = np.zeros( ( const.N_x * const.N_y ), dtype=int) 
    Np_max = 0  # the maximum number of pixels in a cluster
    N_cluster = 0

   

    # loop through all files under d_path
    for root, dirs, files, rootfd in os.fwalk(str(d_path) ):
       """
       if debug: 
          print ( 'root ', root)
          print ( 'dirs ', dirs)
          print ( 'files ', files)
          print ( 'rootfd', rootfd)
       """
       for ifile in sorted(files): 
           #if(debug): print('ifile =', ifile)
           if fnmatch.fnmatch(ifile, d_tag): # data type: clusters
                # clusters.dat file, read in clusters data
                #if(debug): print('d_tag file =', ifile)
                if fnmatch.fnmatch(ifile, det_tag): # det type: [01-16][r-b]
                    #if(debug): print('det_tag = {}, str(det_tag) = {}, repr(det_tag) = {}'.format(  det_tag, str(det_tag), repr(det_tag)))
                    if(debug): print('det_tag file =', ifile)

                    d_file = join(root, ifile) 

                    clusterLists = fIO.loadPixelLists( d_file , False, 'clusters') # get clusters from the input data file

                    m = 0
                    for im in clusterLists: # loop through the five images 
                           N_im = len(im)
                           N_cluster += N_im
                           m +=1
                           #if debug: print (' number of clusters in the {}-th image = {}'.format(m, N_im ) )
                           # get the number of cluster with Np number of pixels
                           for ic in im: 
                              Np = len(ic)
                              if Np > Np_max: Np_max = Np
                              N_cl [Np] += 1

    # plot of the distribution   
    # the array used in plotting 
    x     = np.zeros( ( Np_max + 1), dtype = int)       
    h_Ncl = np.zeros( ( Np_max + 1), dtype = int)
    for i in range(1, Np_max + 1 ): 
       x[i] = i
       h_Ncl[i] = N_cl[i]
       if ( h_Ncl[i] > 0 ): print (x[i] , '\t\t', h_Ncl[i])


    print (x[1], h_Ncl[1], '\t', x[2], h_Ncl[2],  '\t', x[3], h_Ncl[3], '\t',  x[-1], h_Ncl[-1] ) # print out the N_p = 1 bin, and the N_p max bin
    print (' total number of clusters in the input file = ', int(N_cluster) )


    #plt.semilogy(h_Ncl, '-r*')
    plt.loglog(x, h_Ncl, ':ro')
    plt.grid(which='major')
    plt.xlabel('Number of Pixels in Each Event')
    plt.ylabel('Number of Events')
    plt.show()

   

else: 
   print ('the input mode {} is invalid, exit '.format(mode))
   exit(1)



exit
