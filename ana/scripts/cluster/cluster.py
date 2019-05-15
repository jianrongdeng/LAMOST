"""
============================
cluster.py
============================
	date: 20170712 by Jianrong Deng

	purpose:
		cluster class
        modified: 20190513
          add variables to the cluster class: eventType, eventBits, ratio_pVmax_sumpV, ratio_pVmax_avgpV, ratio_pVmax3x3_sumpV, ratio_pVmax5x5_sumpV
============================
"""

"""
The Cluster class inherits from the list class: the pixel list.
It has attributes: 

    data:          data type, ex: 'rb'
    det:           CCD det name, ex: '01b'
    time_stamp:    data taken time
    image_index: the i-th image (there are five bias images). Note: the index starts from 0.
    cluster_index: cluster_index #the i-th cluster in the clusterClass.dat file
    mean:          the biased mean used in the pixel above noise threshold checking
    sstd:          the biased sstd used in the pixel above noise threshold checking

    eventType:     event type, such as "cluster", "loose cluster", "tight cluster", "loose muon", "loose egamma"
    eventBits:     bit map of event type
                   bit     event type
                    0       cluster
                    1       loose cluster
                    2       tight cluster
                    3       loose muon
                    4       tight muon
                    5       loose egamma
                    6       tight egamma
                    7       hot strip
                     
       ex: 
        1. for a tight cluster event, bits 0/1/2 are set, eventBits = 0x 0000 0111 = 2^2 + 2^1 + 2^0 = 7
        2. for a tight muon event, bits 0/1/2/3/4 are set, eventBits = 0x 0001 1111 = 2^0 + 2^1 + 2^2 + 2^3 + 2^4 = 2^5 - 1 = 31

    n_p:           number of pixels in a cluster
    coef:          correlation coefficient
    eigVal:        the float ndarray of the eigen values
    ratio_eigVal:  the short length over the long length, ie: eigVal[0]/eigVal[1]
    w_coef:         correlation coefficient weighted with the pixel value
    w_eigVal:       the float ndarray of the eigen values weighted with the pixel value
    ratio_w_eigVal: the short length over the long length, ie: w_eigVal[0]/w_eigVal[1]
                    for a muon, with a narrow width and a long track, this value will be
                    smaller than electron/gamma events, which have wide widths and short lengths. 

    xs:            # x axis
    xmax:   maximum X value
    xmin:   minimum X value
    deltax: xmax - xmin # delta (X value)

    ys:            # y axis
    ymax:   maximum Y value
    ymin:   minimum Y value
    deltay: ymax - ymin # delta (Y value)

    pVs:            # z (pixel value) axis
    pVmax:   maximum pV
    pVmin:   minimum pV
    deltapV: pVmax - pVmin # delta (pixel value)
    pVmax3x3:   sum of the maximum pV and its 3x3 neighbor pixels' pVs

    #### moments:    the moments up to the third order of a rasterized shape.

    pVs:           list of pixel values
    sumpV:          sum of the pVs in the cluster
    avgpV:          average pVs per pixel in the cluster

    ### pV ratios:
    ratio_pVmax_sumpV:  ratio of pVmax to sumpV
    ratio_pVmax_avgpV:  pVmax/avgpV
    # note: clustering is done with a 3x3 matrix mask
    ratio_pVmax3x3_sumpV: pVmax(3x3 neighboring pixels)/sumpV
    ratio_pVmax3x3_avgpV: pVmax(3x3 neighboring pixels)/avgpV
    #ratio_pVmax5x5_sumpV: 

"""

#import cv2 
import numpy as np
import sys
# add 'commom' directory to python import search path
sys.path.append('../common/')
import stats as st
import const
import tools

#==========================
class Cluster(list):
#==========================
    def __init__(self, filename,  b_mean, b_sstd , image_index, cluster_index,  pixels = []):
#==========================
         '''
         Purpose: initialize a "Cluster" object
         Input:
            filename: -clusters.dat
               ex: rb-01b-20160101174212-clusters.dat'              
            b_mean: the biased mean used in the pixel above noise threshold checking
            b_sstd: the biased sstd used in the pixel above noise threshold checking
            image_index: the i-th image (there are five bias images). 
            cluster_index: the i-th cluster in the clusterClass.dat file
               Note: the index starts from 0.
            pixels:  the pixels in the input cluster   
         Output:
         '''
         # the code to initialize a "Cluster" object.
         list.__init__([])
         # same for clusters in one image:
         tmp = filename.strip().split('-')
         self.data_type = tmp[0]  # data type, ex: 'rb'
         self.det = tmp[1]     # CCD det name, ex: '01b'
         self.time_stamp =tmp[2] # data taken time, ex: '20160101174212'
         self.image_index = image_index #the i-th image (there are five bias images). 
         self.cluster_index = cluster_index #the i-th cluster in the clusterClass.dat file

         self.eventType = 'cluster'
         # set the 'cluster' bit: the 0th bit
         self.eventBits = 0b00000001 # in binary format

         self.mean = b_mean # the biased mean used in the pixel above noise threshold checking
         self.sstd = b_sstd # the biased sstd used in the pixel above noise threshold checking


         # list of pixels
         self.extend(pixels)
         # transversed list:
         ps_T = np.array(pixels).T
         # list of pixel values
         self.xs  = ps_T[0]
         self.ys  = ps_T[1]
         self.pVs = ps_T[2]

         # get max, min, delta
         self.xmin  = np.min(self.xs)
         self.ymin  = np.min(self.ys)
         self.pVmin = np.min(self.pVs)

         self.xmax  = np.max(self.xs)
         self.ymax  = np.max(self.ys)
         self.pVmax = np.max(self.pVs)

         self.deltax  = self.xmax  - self.xmin
         self.deltay  = self.ymax  - self.ymin
         self.deltapV = self.pVmax - self.pVmin

         # the pixel where the pixel value is the maximum in the pixels of the cluster
         pixel_pVmax = getPixel()
         # find the neighbor pixels in a 3x3 matrix with the pixel of the pVmax in the center
         pixels_pVmax3x3 = getPixels3x3(pixel_pVmax)


         # number of pixels in the cluster
         self.n_p = len(pixels)
         # the pearson's correlation coefficient, a measure of the linear correlation of a dataset
         # It has a value between +1 and −1, 
         #  where 1 is total positive linear correlation, 
         #        0 is no linear correlation, 
         #   and −1 is total negative linear correlation
         # the np.corrcoef(data) function returns the coef matrix,
         # where [0,1] is the value of coef_xy
         #self.coef = np.corrcoef (np.array(pixels).T ) [0, 1]
         # coefficients and eigen values
         self.coef, self.eigVal = st.cal_corr(pixels, weight=False)
         # ratio of the short axis to the long axis
         # if self.eigVal[1] == 0:
         #    self.ratio_eigVal =  -1 # set to a negative value
         # else:    
         self.ratio_eigVal = tools.getRatio(  self.eigVal[0], self.eigVal[1], error= -1 )
         # coefficients and eigen values weighted with the pixel value
         self.w_coef, self.w_eigVal = st.cal_corr(pixels, weight=True)
         # ratio of the short axis to the long axis of the weighted eigVals
         self.ratio_w_eigVal = tools.getRatio(  self.w_eigVal[0], self.w_eigVal[1], error= -1 )

         # total energy in the cluster
         self.sumpV = sum(self.pVs)
         # average energy per pixel in the cluster
         self.avgpV = self.sumpV/self.n_p
         # pV ratios:
         #ratio_pVmax_sumpV:  ratio of pVmax to sumpV
         self.ratio_pVmax_sumpV = tools.getRatio(self.pVmax, self.sumpV, error = -1)
         #ratio_pVmax_avgpV:  pVmax/avgpV
         self.ratio_pVmax_avgpV = tools.getRatio(self.pVmax, self.avgpV, error = -1)
         # note: clustering is done with a 3x3 matrix mask
         #ratio_pVmax3x3_sumpV: pVmax(3x3 neighboring pixels)/sumpV
         self.ratio_pVmax3x3_sumpV = tools.getRatio(self.pVmax3x3, self.sumpV, error = -1)
         #ratio_pVmax3x3_avgpV: pVmax(3x3 neighboring pixels)/avgpV
         self.ratio_pVmax3x3_avgpV = tools.getRatio(self.pVmax3x3, self.avgpV, error = -1)
#==========================


#==========================
    def printCluster(self, fn=sys.stdout):
         '''
         input:
            fn: save the print out to file: fn
         output: 
         '''

         import numpy as np
         import sys
         # add 'commom' directory to python import search path
         sys.path.append('../common/')
         # various toos, in: '../common/tools.py'
         import tools

         '''
         # formatting:
         1. '{:4d}'.format(42)
                  Output:  42
         2.  '{:06.2f}'.format(3.141592653589793)
                  Output: 003.14
         '''

         # open output file with "w"
         try:
            with open(fn, 'w' ) as txt_file:
                 print('filename = ', fn, file=txt_file)
                 # the code to print a "Cluster" object.
                 decimals = 1
                 print('data_type = ', self.data_type, ', det = ', self.det, ', time_stamp = ', self.time_stamp, file=txt_file)
                 print('image mean = ', np.round(self.mean, decimals), 'image sstd = ', np.round(self.sstd, decimals), file=txt_file) 
                 print('image_index = ', self.image_index, file=txt_file) 
                 print('cluster_index = ', self.cluster_index, file=txt_file) 
                 print('eventType = ', self.eventType, file=txt_file)
                 print('eventBits = 0B{:012b}'.format( self.eventBits), file=txt_file) # print in binary format
                 print('pixels : ', file=txt_file) 
                 for ip in range(len(self)): 
                     print(ip, ' \t: {:6d}, {:6d}, {:6d}'.format((int)(self[ip][0]), (int)(self[ip][1]), (int)(self[ip][2]), ), file=txt_file) 
                 print('number of pixels in the cluster = ', self.n_p, file=txt_file) 
                 print('xmin = ', (int)(self.xmin), file=txt_file) 
                 print('xmax = ', (int)(self.xmax), file=txt_file) 
                 print('ymin = ', (int)(self.ymin), file=txt_file) 
                 print('ymax = ', (int)(self.ymax), file=txt_file) 
                 print('pVmin = ', np.round(self.pVmin, decimals), file=txt_file) 
                 print('pVmax = ', np.round(self.pVmax, decimals), file=txt_file) 
                 print('sumpV = ', np.round(self.sumpV, decimals), file=txt_file) 
                 print('avgpV = ', np.round(self.avgpV, decimals), file=txt_file) 
                 print('    pVmax/sumpV = {:.2f}'.format( self.ratio_pVmax_sumpV), file=txt_file) 
                 print(' pVmax3x3/sumpV = {:.2f}'.format( self.ratio_pVmax3x3_sumpV), file=txt_file) 
                 print('    pVmax/avgpV = {:.2f}'.format( self.ratio_pVmax_avgpV), file=txt_file) 
                 print(' pVmax3x3/avgpV = {:.2f}'.format( self.ratio_pVmax3x3_avgpV), file=txt_file) 
                 decimals = 2
                 print('correlation coefficient          = ', np.round(self.coef, decimals), file=txt_file) 
                 print('eigen values of the covariance matrix=          [ ', np.round(self.eigVal[0], decimals), ', ', np.round(self.eigVal[1], decimals), ']',  file=txt_file) 
                 print(' eigVal[0]/eigVal[1] = {:.2f}'.format( self.ratio_eigVal), file=txt_file) 
                 print('weighted correlation coefficient = ', np.round(self.w_coef, decimals), file=txt_file) 
                 print('weighted eigen values of the covariance matrix= [ ',np.round(self.w_eigVal[0], decimals), ', ',  np.round(self.w_eigVal[1], decimals),  ']', file=txt_file) 
                 print(' w_eigVal[0]/w_eigVal[1] = {:.2f}'.format( self.ratio_w_eigVal), file=txt_file) 

         except IOError as err:
            print('File error: ', + str(err))
         finally:
            txt_file.close()

#==========================

#==========================
# other functions used in checking clusterLists
#==========================
def GetNumPix(clusterLists):
    """
    purpose: get the distribution of number of pixels for the
    clusterLists
    input : 
       clusterLists: read from :
              clusterLists = fIO.loadPixelLists( infile)
              there will be 5 images in one infile
    output: 
         # the arrays used for plotting, where the range of x-axis is : 1 -  Np_max (inclusively) 
          x: 1 - Np_max, where Np_max is the maximum number of pixels in the clusters
          h_Ncl [Np] : number of cluster events with Np pixels

    """

    # the maximum number of pixels in a cluster = const.N_x * const.N_y
    N_cl      = np.zeros( ( const.N_x * const.N_y ), dtype=int) 

    Np_max = 0  # the maximum number of pixels in a cluster
    # get the number of cluster of Np (number of pixel)
    for ic in clusterLists: 
       Np = len(ic)
       if Np > Np_max: Np_max = Np
       N_cl     [Np] += 1

    # the array used in plotting 
    x     = np.zeros( ( Np_max + 1), dtype = int)       
    h_Ncl = np.zeros( ( Np_max + 1), dtype = int)

    for i in range(1, Np_max + 1 ): 
       x[i] = i
       h_Ncl[i] = N_cl[i]

    return [x, h_Ncl]

#==========================


