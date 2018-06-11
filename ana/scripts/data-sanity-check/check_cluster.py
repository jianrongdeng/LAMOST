
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
import filesIO as fIO # under ../common/ directory



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

    if debug: 
        print ( '\n input list : ')
        print ( 'x \t y \t pValue ')
        for ip in cList:
           print (ip[0], '\t', ip[1], '\t', int(ip[2]))
        print ( ' number of pixels in the cluster = ', len(cList))

    if (len(cList) <= 2 ) : return  # will not plot <= 2-pixel cluster

    # get position_x, position_y vectors from the input cList
    pX = []
    pY = []
    for ip in cList: 
       pX.append( ip[0] )
       pY.append( ip[1] )



    """
    # get axis range
    pX.sort()
    # get axis range
    xmin = int( pX[0]  - 10 ) # " +/-10 " to avoid xmin = xmax
    xmax = int( pX[-1] + 10 )

    pY.sort()
    ymin = int( pY[0]  - 10 ) 
    ymax = int( pY[-1] + 10 )


    #fig = plt.figure()

    #ax = fig.add_axes([xmin, xmax,  ymin, ymax])
    #ax.grid(which='both')
    #plt.axis([float('-inf'), float('inf'),  float('-inf'), float('inf')]) # axis limits  to be set automatically
    """


    ax = plt.figure().gca()
    ax.xaxis.set_major_locator(MaxNLocator(integer=True)) # tick only on integer
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.grid(which='major')
    plt.plot(pX, pY, 'r*')
    plt.show()

    return
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
# check the first five clusters ( one cluster in each image)
for im in clusterLists: # loop through five images 
       N_cluster += len(im)
       for icluster in im: # loop through the clusters
           list2bitMap( icluster, debug )
           N_cluster_analyzed += 1

print (' total number of clusters in the input file = ', int(N_cluster) )
print (' total number of clusters analyzed = ', int(N_cluster_analyzed) )

exit


