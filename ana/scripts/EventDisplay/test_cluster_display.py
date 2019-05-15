'''
============================
test_cluster_display.py
============================

	date: 20190430 by Jianrong Deng
	purpose:
		test cluster_display
============================
'''


import sys
# add 'commom' directory to python import search path
sys.path.append('../common/')
import filesIO as fIO # under ../common/ directory
sys.path.append('../cluster/')
#import cluster # under ../cluster/ directory
import cluster_display as cl_d
import numpy as np

file_cluster = '/Users/jdeng/baiduCloudDisk/LAMOST/ana/outputs/run1_20171205/20160101/bias/rb-01r-20160101174212-clusterClass.dat'

# read clusters from input file
clusters = fIO.loadPixelLists(file_cluster, False, 'clusters')

#debug = False
debug = False
debugL2 = True

if  debug: 
      cl_d.list2graph (clusters[0][0]) # make scatter plot 
      #cl_d.list2TH2F (clusters[0][0]) # make scatter plot 

else:
    # five images
    for im in range(len(clusters)):
        for ic in range(len(clusters[im])): 
        #for ic in clusters[im]:
          clu = clusters[im][ic]
          clu_fn = file_cluster + '_cluster_display' + '_image' +  str(im) + '_Cluster' + str(ic) + '_np' + str(len(clu ))  
          ### mark hot-strip events
          if clu.eigVal[0] == 0:
              pixel_xy =  '_x_' + str(int(clu.xmin)) + '-' + str(int(clu.xmax)) + '_y_' + str(int(clu.ymin)) + '-' + str(int(clu.ymax))  # strip location
              clu_fn = clu_fn + pixel_xy + '_hotstrip'
          else:
              ### mark large sumpV events
              if clu.sumpV > 1e5:         
                  sumpV = '_sumpV_' + str(int(clu.sumpV)) 
                  clu_fn = clu_fn + sumpV
              else:
                  ### mark large w_eigVal[1] events (long muon tracks)
                  if clu.w_eigVal[1] > 80:
                     w_eigVal_1 = '_w_eigVal_1_' + str(np.round(clu.w_eigVal[1], 1))
                     clu_fn = clu_fn + w_eigVal_1
                  else:
                      ### mark large pV events
                      if clu.pVmax > 1e4: 
                         pVmax = '_pVmax_' + str(int(clu.pVmax))
                         clu_fn = clu_fn + pVmax
             
          graph_filename  = clu_fn + '_graph.eps'
          hist2F_filename = clu_fn + '_hist2F.eps'
          txt_filename    = clu_fn + '.txt'
          cl_d.list2graph (clusters[im][ic], True, graph_filename, txt_filename) # make scatter plot 
          #cl_d.list2TH2F (clusters[im][ic], True, hist2F_filename, txt_filename) # make scatter plot 


