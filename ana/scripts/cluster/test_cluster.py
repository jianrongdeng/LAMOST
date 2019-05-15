"""
============================
test_cluster.py
============================

	date: 20171202 by Jianrong Deng
	purpose:
		test the cluster class
============================
"""


import sys
# add 'commom' directory to python import search path
sys.path.append('../common/')
import filesIO as fIO # under ../common/ directory
import const
import cluster 
import h_clusterClass as hcl

debug = False
debug_L2 = True

file_cluster = '/Users/jdeng/baiduCloudDisk/LAMOST/ana/outputs/run1_20171205/20160101/bias/rb-01b-20160101174212-clusters.dat'
file_stat    = '/Users/jdeng/baiduCloudDisk/LAMOST/ana/outputs/run1_20171205/20160101/bias/rb-01b-20160101174212-stat.dat'
# get the filename of the cluster file (without pathname)
tmp_a = file_cluster.strip().split('/')
filename = tmp_a[-1]
# read stat info from stat file
stat = fIO.loadStat(file_stat, debug)
# read clusters from input file
clusterLists = fIO.loadPixelLists(file_cluster, False, 'clusters')

# clusters in the cluster Class data format
cls = []
for im in range(const.N_b): cls.append([]) # clusterClass for the five images

# five images
for im in range(len(clusterLists)):
    # number of cluster in one image analyzed:
    nCl = 0
    #if (debug_L2): print (clusterLists[im])
    # clusters in each image
    for ic in clusterLists[im]: 
       nCl  = nCl + 1
       if (debug ): 
          if ( nCl == 1 ): break
       #if (debug_L2): print (ic)
       # skip clusters with the number of pixel == 1
       if len(ic)==1: continue
       # fill in the cluster class
       icluster = cluster.Cluster(filename, stat[im][0], stat[im][1], im, nCl,  ic) 
       # histogram various distribution of the cluster class
       # more than 30 pixel in the cluster
       if (icluster.n_p > 30) : 
           if(debug_L2): icluster.printCluster()

       cls[im].append(icluster)
   

# fill tree
hcl.FillClusterTree(cls)




