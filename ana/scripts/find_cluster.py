"""
============================
script: find_cluster.py
============================
	date: 20170612 by Jianrong Deng
	purpose:
		read in a mask file (made by hot_cell_mask.py), find 3x3 clusters using the mask
	Input: mask file
	Output: cluster lists
        Note: (generated in hot_cell_mask.py )
            definition: mask = np.zeros((N_y, N_x),dtype=int )    # array to save the bitmap of each pixel
            bitmap:     mask[iy,ix] = bits.setBit(mask[iy, ix], it)  # if > 3sigma, set the it-th bit to 1
"""

#import numpy as np
import const  # constants used in LAMOST image processing
import bits   # bit manipulate function

#============================
def findCluster(mask, hotcell, iy, ix, pixelFlag, pixels, im=0):
    """
    purpose: findCluster of pixel (iy, ix)
    input: 
         mask  matrix
         hotcell matrix
         pixel position (iy, ix), 
         pixelFlag: np.(Ny, Nx), value(iy, ix) set to 1 if pixel(iy, ix) is already checked
         pixels: already found pixels in the cluster
         im: image index (default is the first image)
    output: 
         pixels: cluster in pixel-list (using 3x3 cluster to check neighboring pixels)
    Usage: use findCluster recursively to get cluster, see example in ana_clusters.py     
    """
    # check if it is a valid pixel position
    if (not isPixel(iy, ix)): 
        print ('Error: calling function findCluster() for a non-PIXEL position')
        return

    # if it is a hotcell, ignore
    if hotcell[iy, ix] == 1:  return pixels

    # if pixel(iy, ix) is already checked, do nothing
    if (pixelFlag[iy, ix] == 1): return pixels

    # if not checked yet
    pixelFlag[iy, ix] =  1              # flag pixel(iy, ix) as checked
    # checked if it is an above threshold pixel:
    if (bits.testBit(mask[iy, ix], im) ): 
         pixels.append([iy, ix])            # if yes, add to cluster
         # now check its neighbor pixels
         nbr = getNeighbor(iy, ix)
         for ip in nbr:
                  findCluster(mask, hotcell, ip[0], ip[1], pixelFlag, pixels, im)
    return pixels 

#============================
def isPixel(iy, ix):
    """
    purpose: check if (iy, ix) is a valid pixel: within image boundary
    input: position (iy, ix)
    output: True or False
    """
    isP = True
    if ( ix < 0 or ix > (const.N_x - 1) or iy < 0 or iy > (const.N_y - 1)):
       isP = False
    return isP

#============================
def isCorner(iy, ix):
    """
    purpose: check if pixel (iy, ix) is at corner
    input: pixel position (iy, ix)
    output: True if is Corner pixel
    """
    isC = False

    if   ( ix ==0              and iy == 0             ): isC = True
    elif ( ix ==0              and iy == const.N_y - 1 ): isC = True
    elif ( ix == const.N_x - 1 and iy == 0             ): isC = True
    elif ( ix == const.N_x - 1 and iy == const.N_y - 1 ): isC = True

    return isC


#============================
def isEdge(iy, ix):
    """
    purpose: check if pixel (iy, ix) is on the edge
    input: pixel position (iy, ix)
    output: True if is an edge-pixel
    """
    # first check if it is a corner-pixel
    if isCorner(iy, ix): return False

    isE = False

    if   ( ix ==0                ): isE = True
    elif ( ix == (const.N_x - 1) ): isE = True
    elif ( iy ==0                ): isE = True
    elif ( iy == (const.N_y - 1) ): isE = True

    return isE


#============================
def getNeighbor(iy, ix):
    """
    purpose: get neighbor pixels of an input pixel (iy, ix) 
    input: pixel position (iy, ix)
    output: list of neighbor pixels
    """
    if isPixel(iy, ix):
        if isCorner(iy, ix): return getCornerNeighbor(iy, ix)
        elif isEdge(iy, ix): return getEdgeNeighbor(iy, ix)
        else:
            nbr =  []
            nbr.append([iy-1, ix-1])
            nbr.append([iy  , ix-1])
            nbr.append([iy+1, ix-1])
            nbr.append([iy-1, ix  ])
            nbr.append([iy+1, ix  ])
            nbr.append([iy-1, ix+1])
            nbr.append([iy  , ix+1])
            nbr.append([iy+1, ix+1])
            return nbr             
    else: 
        print ('Error: calling function getNeighbor() for a non-PIXEL position')


#============================
def getCornerNeighbor(iy, ix):
    """
    purpose: get neighbor pixels of an input CORNER pixel (iy, ix) 
    input: CORNER pixel position (iy, ix)
    output: list of neighbor pixels
    """
    nbr =  []
    if isCorner(iy, ix): 
        if   ( ix == 0 and iy == 0 ):
            nbr.append([1, 0])
            nbr.append([0, 1])
            nbr.append([1, 1])
        elif ( ix == 0 and iy == const.N_y - 1  ):
            nbr.append([const.N_y - 2 ,0])
            nbr.append([const.N_y - 1 ,1])
            nbr.append([const.N_y - 2 ,1])
        elif ( ix == const.N_x - 1 and iy == 0  ): 
            nbr.append([0, const.N_x - 2 ])
            nbr.append([1, const.N_x - 2 ])
            nbr.append([1, const.N_x - 1 ])
        elif ( ix == const.N_x - 1 and iy == const.N_y -1 ): 
            nbr.append([const.N_y - 2, const.N_x - 2 ])
            nbr.append([const.N_y - 1, const.N_x - 2 ])
            nbr.append([const.N_y - 2, const.N_x - 1 ])

        return nbr
    else : 
       print ('Error: calling function getCornerNeighbor() for a non-CORNER pixel')


#============================
def getEdgeNeighbor(iy, ix):
    """
    purpose: get neighbor pixels of an input EDGE pixel (iy, ix) 
    input: EDGE pixel position (iy, ix)
    output: list of neighbor pixels
    """
    nbr =  []
    if isEdge(iy, ix): 
        if   ( ix ==0                ):           
            nbr.append([iy - 1, 0])
            nbr.append([iy + 1, 0])
            nbr.append([iy - 1, 1])
            nbr.append([iy    , 1])
            nbr.append([iy + 1, 1])
        elif ( ix == (const.N_x - 1) ):           
            nbr.append([iy - 1, const.N_x - 2])
            nbr.append([iy    , const.N_x - 2])
            nbr.append([iy + 1, const.N_x - 2])
            nbr.append([iy - 1, const.N_x - 1])
            nbr.append([iy + 1, const.N_x - 1])
        elif ( iy ==0                ):           
            nbr.append([0, ix - 1])
            nbr.append([1, ix - 1])
            nbr.append([1, ix    ])
            nbr.append([0, ix + 1])
            nbr.append([1, ix + 1])
        elif ( iy == (const.N_y - 1) ):           
            nbr.append([const.N_y - 2, ix - 1])
            nbr.append([const.N_y - 1, ix - 1])
            nbr.append([const.N_y - 2, ix    ])
            nbr.append([const.N_y - 2, ix + 1])
            nbr.append([const.N_y - 1, ix + 1])
        return nbr
    else : 
       print ('Error: calling function getEdgeNeighbor() for a non-EDGE pixel')

