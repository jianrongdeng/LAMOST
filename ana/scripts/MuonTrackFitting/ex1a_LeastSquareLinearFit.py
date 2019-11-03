'''
============================
ex1a_LeastSquareLinearFit.py
============================
  Date: 20191014 by Jianrong Deng

  Purpose: an example of a linear fit using the least square method

  Method: use numpy.linalg.lstsq
          " Solves the equation a x = b by computing a vector x that minimizes the squared Euclidean 2-norm \| b - a x \|^2_2"
  Reference: https://docs.scipy.org/doc/numpy/reference/generated/numpy.linalg.lstsq.html#numpy.linalg.lstsq
  
  Note: Modified from example: ex1_LeastSquareLinearFit.py
  Modification: 
      read in input array from a given data file in.dat, which is an
      data file created 
      by using the function: dumpData(data_out = in.dat, ...) 
      in the module  ../pickle_data/pickle_data.py,
      The data file includes a list of pixels, each pixel has [x, y, pV]. 

  Input: 
     a given pickle data file, with at least two columns of data, the first column is X, the second column is Y

  Output: fitting parameters of the line
        y = mx + c
	residuals = sums of residuals
	normalized residuals = sums of residuals / len(x)
  Plot: data points vs fitting line

  Usage: python ex1a_LeastSquareLinearFit.py

============================
============================
'''

import sys
# add 'pickle_data' directory to python import search path
sys.path.append('../pickle_data/')
import pickle_data as pd
data_dir = '../pickle_data/test_pickle_data_20190806/'
data_in =   data_dir +  'pickle_load.dat'
txt_out =   data_dir +  'data.txt'
pixels =pd.loadData(data_in, debug = True, data_type='list', txt_fn=txt_out)

import numpy as np
#x = np.array([0, 1, 2, 3])
#y = np.array([-1, 0.2, 0.9, 2.1])
data = np.asarray(pixels)
data = data.T
x = data[0]
y = data[1]
# pixel readout value of each pixel in the list
pV = data[2]

Nx = len(x)
A = np.vstack([x, np.ones(len(x))]).T
m, c = np.linalg.lstsq(A, y)[0]
verbose = 1
if(verbose):
  print('x = ', x)
  print('y = ', y)
  print('pV = ', pV)
  print('len(x) = ', Nx)

print('y = m*x + c:  m= ', m, '; c= ', c)
res = np.linalg.lstsq(A, y)[1]
if(Nx >=1 ):
    print ('res =', res, ';\t normalized res = res/len(x) = ', res/Nx)
import matplotlib.pyplot as plt
_ = plt.plot(x, y, 'o', label='Original data', markersize=10)
_ = plt.plot(x, m*x + c, 'r', label='Fitted line')
_ = plt.legend()
plt.show()

