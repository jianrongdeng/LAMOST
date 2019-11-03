'''
============================
ex1b_LeastSquareLinearFit.py
============================
  Date: 20191014 by Jianrong Deng

  Purpose: an example of a linear fit using the least square method

  Method: use numpy.linalg.lstsq
          " Solves the equation a x = b by computing a vector x that minimizes the squared Euclidean 2-norm \| b - a x \|^2_2"
  Reference: https://docs.scipy.org/doc/numpy/reference/generated/numpy.linalg.lstsq.html#numpy.linalg.lstsq
  
  Note: Modified from example: ex1a_LeastSquareLinearFit.py
  Modification: 
      Do a 90 degree clock-wised rotation from the image coordinates
      to the horizontal-vertical coordinates. 
      Image coordinates: 
         x: 0 - 4096 + 2 * overscan regions (32 channels each) = [0, 4160]
         y: 0 - 4096 channels

      The x axis corresponds to the 250 fibers, which counts from 0
      (left in the image) to 250 (right in the image).
      In the setup of the fibers, it counts from 0 (top in the setup)
      to 250 (down in the setup). 

      After 90-degree clockwised rotation, 
      y -> horizontal [0, 4096]
      x -> vertical [0, 4160]

      The data file includes a list of pixels, each pixel has [x, y, pV], which transforms to [h, v, pV], where:
      h: horizontal [0, 4096]
      v: vertical   [0, 4160]
  Input: 
     a given pickle data file, with at least two columns of data, the first column is X, the second column is Y

  Output: fitting parameters of the line
        v = hx + c
	residuals = sums of residuals
	normalized residuals = sums of residuals / len(x)
  Plot: data points vs fitting line

  Usage: python ex1b_LeastSquareLinearFit.py

============================
============================
'''


#============================
def LeastSquareLinearFit_90degreeCWRotation(pixels):
#============================


    import numpy as np
    #x = np.array([0, 1, 2, 3])
    #y = np.array([-1, 0.2, 0.9, 2.1])
    data = np.asarray(pixels)
    data = data.T
    x = data[0]
    y = data[1]
    h = y # y is horizontal
    v = x # x is vertical
    # pixel readout value of each pixel in the list
    pV = data[2]

    Nh = len(h)
    A = np.vstack([h, np.ones(len(h))]).T
    #Solves the equation a x = b by computing a vector x that minimizes the squared Euclidean 2-norm \| b - a x \|^2_2.
    # where b = v, A = [h, 1], x = [m, c].T
    #Reference: https://docs.scipy.org/doc/numpy/reference/generated/numpy.linalg.lstsq.html#numpy.linalg.lstsq
    fit = np.linalg.lstsq(A, v)
    m, c = fit[0] # fit: v' = m*h + c
    verbose = 1
    if(verbose):
      print('h = ',  h)
      print('v = ',  v)
      print('pV =', pV)
      print('len(h) = ', Nh)

    print('v = m*h + c:  m= {:.1f}; c= {:.1f}'.format( m,  c))
    # residuals: Sums of residuals; squared Euclidean 2-norm for each column in b - a*x, i.e.:  ( v - ( m*h + c ) )^2 = (v - v')^2
    res = fit[1][0]
    res_normalized = -1
    if(Nh >=1 ):
        res_normalized = res/Nh
        #print ('res = {:f}; \t normalized res = res/len(h) = {:f} '.format( res, res_normalized ))
        print ('res = {:.1f}; \t normalized res = res/len(h) = {:.1f} '.format( res, res_normalized ))
    import matplotlib.pyplot as plt
    _ = plt.plot(h, v, 'o', label='Original data: vertical = m*horizontal + c', markersize=10)
    _ = plt.plot(h, m*h + c, 'r', label='Fitted line')
    _ = plt.legend()
    plt.show()

    return fit
#============================

'''
============================
def Cartesian2SphericalCoordinates(m, c):
#============================
============================
  Date: 20191022 by Jianrong Deng

  Purpose: convert cartesian coordinates to spherical coordinates

  Method: 

  Input: v = m * h + c, the linear fit parameters: m and c

  Output: the zenith angle theta in the range of [-pi/2, pi/2]

#============================
'''
#============================
def zenithAngle(m, c):
    
    import numpy as np

    v0 = m * 0 + c
    h0 =  (0 - c ) / m 
    if (v0 == 0): 
       theta = 90
    else:
       # arctan returns an angle in the range of [-pi/2, pi/2]
       # theta in degree
       # the minus sign "-" set the theta > 0 for a track of (h1, v1 ) --> (h2, v2) with (h2 > h1, v2>v1)
       theta = np.arctan( -h0/v0 ) / (np.pi) * 180

    print('zenith angle theta = {:.1f}'.format( theta ))

    return theta
#============================

#============================
# main
#============================


import sys
# add 'pickle_data' directory to python import search path
sys.path.append('../pickle_data/')
import pickle_data as pd
data_dir = '../pickle_data/test_pickle_data_20190806/'
data_in =   data_dir +  'pickle_load.dat'
txt_out =   data_dir +  'data.txt'
pixels =pd.loadData(data_in, debug = True, data_type='list', txt_fn=txt_out)

fit = LeastSquareLinearFit_90degreeCWRotation(pixels)
m, c = fit[0]
zenithAngle(m, c)


