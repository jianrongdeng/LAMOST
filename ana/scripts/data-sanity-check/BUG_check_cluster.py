
"""
============================
check_cluster.py
============================
	date: 20180524 by Jianrong Deng
        Purpose: 
	   input: read in a '-clusters,dat' data file
           output: convert a selected cluster (in a list format ) to a 2D bit map
============================
"""
import sys
# add 'commom' directory to python import search path
sys.path.append('../common/')
import stats as st
import filesIO as fIO # under ../common/ directory
import numpy as np



#============================
def list2bitMap (cList, debug = False) : 
#============================
    """
    purpose: convert a list to a bit map
    input : 
       cList: a list of pixels ( x, y, pValue )
       debug: debugging flag
    output: bitMap 

    """
   
    import matplotlib.pyplot as plt
    from matplotlib.ticker import MaxNLocator


    n_p = len(cList)

    if ( n_p <= 200 ) : return  # will not plot <= 200-pixel cluster
    if debug: 
        print ( '\n input list : ')
        print ( 'x \t y \t pValue ')
        for ip in cList:
           if (ip[2] > 1000): 
               print (ip[0], '\t', ip[1], '\t', int(ip[2]))

    print ( ' number of pixels in the cluster = ', n_p )

    # get position_x, position_y vectors from the input cList
    data = np.array(cList).T
    pX = data[1] # to match DS9, x <-> y switch
    pY = data[0] # to match DS9, x <-> y switch
    #pV = data[2]

    


    # get axis range
    pX.sort()
    # get axis range
    xmin = int( pX[0]  - 5 ) # " +/-5 " to avoid xmin = xmax
    xmax = int( pX[-1] + 5 )
    delta_x = xmax - xmin

    pY.sort()
    ymin = int( pY[0]  - 5 ) 
    ymax = int( pY[-1] + 5 )
    delta_y = ymax - ymin

    # keep the scale of x and y: 
    # ie: the same number of bins in x and y, so the shape of a line won't  be distorted
    
    if (delta_x > delta_y): 
       patch = int( (delta_x - delta_y)/2 )
       ymin = ymin - patch
       ymax = ymax + patch
    else: 
       patch = int( (delta_y - delta_x)/2 )
       xmin = xmin - patch
       xmax = xmax + patch


    #fig = plt.figure()

    #ax = fig.add_axes([xmin, xmax,  ymin, ymax])
    #ax.grid(which='both')
    #plt.axis([float('-inf'), float('inf'),  float('-inf'), float('inf')]) # axis limits  to be set automatically


    ax = plt.figure().gca()
    ax.xaxis.set_major_locator(MaxNLocator(integer=True)) # tick only on integer
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_ylim(ymin, ymax)
    ax.set_xlim(xmin, xmax)
    plt.grid(which='major')
    #plt.plot(data[0], data[1], 'r*')
    plt.plot(data[1], data[0], 'r*')  # to match DS9, x <-> y switch



    # check correlation
    coef, eigVal = st.cal_corr(cList, weight=False)
    coef_txt = '   coef='+ str(coef) + ',      eigV = ' + str(eigVal)
    w_coef, w_eigVal = st.cal_corr(cList, weight=True)
    w_coef_txt = 'w_coef='+ str(w_coef) + ', w_eigV = ' + str(w_eigVal)
    np_txt = 'number of pixels = '+str(n_p)
    print(coef_txt)
    print(w_coef_txt)
    print(np_txt)
    plt.text(xmin, ymax+1, coef_txt)
    plt.text(xmin, ymax+(ymax-ymin)/10, w_coef_txt)
    plt.text((xmin+xmax)/2 + 2, (ymin +ymax)/2 - 5, np_txt)

    #ax.scatter(data[0], data[1], s=np.sqrt(data[2]), label=coef_leg)
    #ax.scatter(data[0], data[1], s=data[2]/10.)  # the size of scatter point proportial to qV data[2]
    # switch x <-> y:
    ax.scatter(data[1], data[0], s=data[2]/10.)  # the size of scatter point proportial to qV data[2]
    plt.legend()



    plt.show()

    return


    """
    # calculate correlation coefficient, see test/test_covariance 
    #coef = np.corrcoef([pX, pY])[0, 1]
    np_coef = np.corrcoef(data)[0, 1]
    print('np.corrcoef: the linear correlation coefficient =', np_coef)
    # calculate coef without weights, 
    # note: the w_coef takes the original List, not the transposed matrix
    #coef = st.w_coef(cList, weight=False)
    #print('the linear correlation coefficient =', coef)


    # calculate the covariance matrix without WEIGHT
    cov = st.w_cov(cList, weight=False)
    # weighted coeff 
    #coef = st.w_coef(cov)
    #print('the linear correlation coefficient =', coef)
    # calculate the eigenValues of the covariance matrix
    eigVal = st.eig(cov, eigvals_only=True)
    print('the eigValues =', eigVal)

    # calculate weighted covariance matrix, use the vector pV as weights
    w_cov = st.w_cov(cList, weight=True)
    # weighted coeff 
    w_coef = st.w_coef(w_cov)
    print('the WEIGHTED linear correlation coefficient =', w_coef)
    w_eigVal = st.eig(w_cov)
    print('the WEIGHTED eigValues =', w_eigVal)
    """
#============================


#============================
# main function
#============================
#

debug = True

# use 'input' to get the input data filename
d_file = input('Enter the name of the *-clusters.dat file to be checked: ')

# clusters.dat file, read in clusters data
clusterLists = fIO.loadPixelLists( d_file , False, 'clusters') # get clusters from the input data file

N_cluster = 0
N_cluster_analyzed = 0
N_im = 0  # the image index
# check the first five clusters ( one cluster in each image)
for im in clusterLists: # loop through five images 
       N_cluster += len(im)
       N_im += 1   
       print ('the N_im =', N_im, '  image')
       for icluster in im: # loop through the clusters
           list2bitMap( icluster, debug )
           N_cluster_analyzed += 1


print (' total number of clusters in the input file = ', int(N_cluster) )
print (' total number of clusters analyzed = ', int(N_cluster_analyzed) )

exit


