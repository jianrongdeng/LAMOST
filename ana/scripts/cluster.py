"""
============================
cluster.py
============================
	date: 20170712 by Jianrong Deng
	purpose:
		cluster class
============================
"""

"""
The Cluster class inherits from the list class: the pixel list.
It has attributes: 
    n_p:           number of pixels in a cluster

    xs:            # x axix
    maxX:   maximum X value
    minX:   minimum X value
    deltaX: maxY - minY # delta (Y value)

    ys:            # y axis
    maxY:   maximum Y value
    minY:   minimum Y value
    deltaY: maxY - minY # delta (Y value)

    moments:    the moments up to the third order of a rasterized shape.

    pVs:           list of pixel values
    sumE:          total energy in the cluster
    avgE:          average energy per pixel in the cluster
    maxE:          maximum pixel value
    minE:          minimum pixel value
    deltaE:        maxE - minE

    mean:          the biased mean used in pixel above noise threshold checking
    sstd:          the biased sstd used in pixel above noise threshold checking

"""

import cv2 

class Cluster(list):
    def __init__(self, b_mean, b_sstd , pixels = []):
         list.__init__([])
         self.mean = b_mean
         self.sstd = b_sstd
         # list of pixels
         self.extend(pixels)
         # number of pixels in the cluster
         self.n_p = len(pixels)
         # list of pixel values
         self.pVs = []
         self.ys = [] # y axis
         self.xs = [] # x axix
         for ip in pixels: 
             self.pVs.append(ip[2])
             self.Ys.append(ip[0])
             self.Xs.append(ip[1])
         # total energy in the cluster
         self.sumE = sum(self.pVs)
         # average energy per pixel in the cluster
         self.avgE = self.sumE/self.np
         tmp = self.pVs.copy()
         tmp.sort(reverse=True)
         self.maxE = tmp[0]  # maximum pixel value
         self.minE = tmp[-1] # minimum pixel value
         self.deltaE = self.maxE - self.minE # delta (pixel value)

         tmp = self.Ys.copy()
         tmp.sort(reverse=True)
         self.maxY = tmp[0]  # maximum Y value
         self.minY = tmp[-1] # minimum Y value
         self.deltaY = self.maxY - self.minY # delta (Y value)

         tmp = self.Xs.copy()
         tmp.sort(reverse=True)
         self.maxX = tmp[0]  # maximum Y value
         self.minX = tmp[-1] # minimum Y value
         self.deltaX = self.maxX - self.minX # delta (Y value)

         self.moments = cv2.moments(pixels)

