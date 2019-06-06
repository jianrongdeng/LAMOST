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
#import h_clusterClass as hcl
import cluster_cut as cl_cut
import numpy as np

sys.path.append('../hist/')
import h_cluster


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
# input files
file_stat = os.environ['env_filename_stat']
if DEBUG:
    print('file_stat :', file_stat)
file_cluster = fIO.setFilename(file_stat, in_tag='stat.dat', out_tag='clusters.dat')
# get the filename of the cluster file (without pathname)
tmp_a = file_cluster.strip().split('/')
filename = tmp_a[-1]
date = filename[7:15]
# output directory
out_path=os.environ['env_path_out'] + '/' + date + '/bias/'
if DEBUG:
    print('out_path :', out_path)
# if the directory does not exist, make the directory
if os.access(out_path, 0) == False:  # access(path, mode), set mode = 0
    os.makedirs(out_path, exist_ok=True)
# output files
file_clusterClass = fIO.setFilename(filename, in_tag='stat.dat', out_tag='clusterClass.dat', out_path=out_path)
file_clustertxt = fIO.setFilename(filename, in_tag='stat.dat', out_tag='clusterClass.txt', out_path=out_path)
file_clusterROOT = fIO.setFilename(filename, in_tag='stat.dat', out_tag='clusterClass.root', out_path=out_path)

if DEBUG:
    print('file_clusters :', file_cluster)
    print('file_clusterClass :', file_clusterClass)
    print('file_clusterROOT :', file_clusterROOT)


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

   
# open output file with "w"
try:
    with open(file_clustertxt, 'w' ) as txt_file:
         #print('filename = ', fn, file=txt_file)
         print('det= {:s}, n_cluster_cand in the {:d} images = {:4d} , in each image: [{:4d}, {:4d}, {:4d}, {:4d}, {:4d}]'.format( cls[0][0].det, im+1, np.sum(nCl), nCl[0], nCl[1], nCl[2], nCl[3], nCl[4] ), file=txt_file)
         print('det= {:s}, n_cluster_cand in the {:d} images = {:4d} , in each image: [{:4d}, {:4d}, {:4d}, {:4d}, {:4d}]'.format( cls[0][0].det, im+1, np.sum(nCl), nCl[0], nCl[1], nCl[2], nCl[3], nCl[4] ))
#         print('det= {:s}, n_cluster_cand in the {:d} images = {:4d} , in each image: [{:4d}, {:4d}, {:4d}, {:4d}, {:4d}]'.format( cls[0][0].det, im+1, np.sum(nCl), nCl[0], nCl[1], nCl[2], nCl[3], nCl[4] ))

except IOError as err:
    print('File error: ', + str(err))
finally:
    txt_file.close()


# save results
# save clusterClass to file			  
# 5 lists of clusters from 5 images save in one file
if DEBUG:
    print('dump clusterClass to file')
    #print('number of clusters found = ', len(cls[0]) )
fIO.dumpPixelLists(file_clusterClass, cls)


# ROOT histograms
from ROOT import TFile
from ROOT import gROOT, gStyle
# root style
gStyle.SetOptStat(11111111) 
gStyle.SetLineColor(2) 
gStyle.SetLineWidth(4) 
gStyle.SetMarkerColor(3) 
gStyle.SetMarkerStyle(21) 
gROOT.ForceStyle() 

rootfile=file_clusterROOT
hfile = gROOT.FindObject(rootfile)
if hfile:
   hfile.Close()
hfile = TFile( rootfile, 'RECREATE', 'ROOT file for the cluster class' )
# initialize the h_cluster class
hcl = h_cluster.h_cluster()

# fill the h_cluster class
# five images
for im in cls: 
# clusters in each image
   for ic in im: 
       hcl.Fill(ic)

# destroy cache, close rootfiles
hcl.destroyCache()

hfile.Write()
# Note that the file is automatically closed when application terminates
# or when the file destructor is called.


# time stamp: 
t_stop = time.ctime()
t_stop_clock = time.clock()
t_running = t_stop_clock - t_start_clock
#print( "Run starts. Current local time is  {} ".format(t_start))
# print ("Run stop. Current local time is  {} ".format(t_stop))
# print ("Total running time is  {} minutes".format(t_running/60 ))

