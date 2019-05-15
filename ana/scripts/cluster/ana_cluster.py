"""
============================
ana_cluster.py
============================
	date: 20171226 by Jianrong Deng
	purpose:
		analyze the pixel-clusters, develop muon selection criteria. 
        Input: cluster list
        Output: cluster data in cluster Class format
============================
"""

import time
import sys
# add 'commom' directory to python import search path
sys.path.append('../common/')
import filesIO as fIO # under ../common/ directory
import const
import os
import cluster 
import h_clusterClass as hcl
import cluster_cut as cl_cut
import numpy as np


#============================
# main program
#============================

DEBUG = False

# time stamp: 
t_start = time.ctime()
t_start_clock = time.clock()
# print( "Run starts. Current local time is  {} ".format(t_start))


# input / output filenames
#set input / output files using environment variables, create output directory if not already exist
# input file for saving cluster lists (one file for 5 lists)
file_stat = os.environ['env_filename_stat']
file_cluster = fIO.setFilename(file_stat, in_tag='stat.dat', out_tag='clusters.dat')
file_clusterClass = fIO.setFilename(file_stat, in_tag='stat.dat', out_tag='clusterClass.dat')
file_clusterROOT = fIO.setFilename(file_stat, in_tag='stat.dat', out_tag='clusterClass.root')

if DEBUG:
    print('file_clusters :', file_cluster)
    print('file_clusterClass :', file_clusterClass)
    print('file_clusterROOT :', file_clusterROOT)


# get the filename of the cluster file (without pathname)
tmp_a = file_cluster.strip().split('/')
filename = tmp_a[-1]
# read stat info from stat file
stat = fIO.loadStat(file_stat, DEBUG)
# read clusters from input file
clusterLists = fIO.loadPixelLists(file_cluster, False, 'clusters')


# clusters in the cluster Class data format
cls = []
nCl = []
for im in range(const.N_b): 
    cls.append([]) # clusterClass for the five images
    nCl.append([]) # number of cluster candidates for the five images


# five images
for im in range(len(clusterLists)):
    # number of cluster analyzed in one image:
    nCl[im] = 0
    #if (debug_L2): print (clusterLists[im])
    # clusters in each image
    for ic in clusterLists[im]: 
       # in debug mode, only check the first cluster
       if (DEBUG ): 
          if ( nCl[im] == 1 ): break
       #if (debug_L2): print (ic)
       # Apply n_p cut
       if ( len(ic) > cl_cut.np): 
           # fill in the cluster class variables
           icluster = cluster.Cluster(filename, stat[im][0], stat[im][1], im, nCl[im], ic) 
           # a few selection cuts to reduce noise
           # avgpV sumpV cuts
           if (icluster.sumpV > cl_cut.sumpV ): 
               if (icluster.avgpV > cl_cut.avgpV ): 
                   cls[im].append(icluster)

                   nCl[im]  = nCl[im] + 1  # number of clusters found

   
print('det=', cls[0][0].det, ', n_cluster_cand in', im+1, 'images = \t', np.sum(nCl), ', in each image:\t', nCl)

# fill root file
hcl.FillClusterTree(cls, file_clusterROOT)

# save results
# save clusterClass to file			  
# 5 clusters from 5 images save in one file
if DEBUG:
    print('dump clusterClass to file')
    #print('number of clusters found = ', len(cls[0]) )
fIO.dumpPixelLists(file_clusterClass, cls)


# time stamp: 
t_stop = time.ctime()
t_stop_clock = time.clock()
t_running = t_stop_clock - t_start_clock
#print( "Run starts. Current local time is  {} ".format(t_start))
# print ("Run stop. Current local time is  {} ".format(t_stop))
# print ("Total running time is  {} minutes".format(t_running/60 ))
