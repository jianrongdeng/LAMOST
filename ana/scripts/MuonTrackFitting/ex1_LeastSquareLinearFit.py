'''
============================
ex1_LeastSquareLinearFit.py
============================
  Date: 20191010 by Jianrong Deng
  Purpose: an example of a linear fit using the least square method
  Method: use numpy.linalg.lstsq
          " Solves the equation a x = b by computing a vector x that minimizes the squared Euclidean 2-norm \| b - a x \|^2_2"
  Reference: https://docs.scipy.org/doc/numpy/reference/generated/numpy.linalg.lstsq.html#numpy.linalg.lstsq
  Input: array x and y
  Output: fitting parameters of the line m and c where: y = mx + c
	residuals = sums of residuals
        residuals = sums of ( y_i - fit_y_i )^2
  Plot: data points vs fitting line

============================
============================
'''



import numpy as np
x = np.array([0, 1, 2, 3])
y = np.array([-1, 0.2, 0.9, 2.1])
Nx = len(x)
A = np.vstack([x, np.ones(len(x))]).T
m, c = np.linalg.lstsq(A, y)[0]
verbose = 1
if(verbose):
  print('x = ', x)
  print('y = ', y)
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

