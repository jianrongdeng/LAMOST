'''
============================
============================
ex2_LeastSquarePolynomialFit.py
============================
  Date: 20191012 by Jianrong Deng
  Purpose: an example of a polynomial fit using the least square method
  Method: use numpy.polynomial.polynomial.Polynomial.fit
  Reference: 
  	https://docs.scipy.org/doc/numpy/reference/generated/numpy.polynomial.polynomial.Polynomial.fit.html#numpy.polynomial.polynomial.Polynomial.fit

  Input: 
        array x and y: sample points (x_i, y_i)
	deg: degree of the fitting polynomials
	    all terms up to and including the deg'th term are included in the fit
  Output: 
        series: fitting parameters of the polynomial
	residuals = sums of squared residuals of the lease squares fit
  Plot: data points vs fitting polynomial

============================
============================

'''



import numpy as np
x = np.array([0, 1, 2, 3])
y = np.array([-1, 0.2, 0.9, 2.1])

deg = 1  # deg = 1: this is a linear fit

polyfit = np.polynomial.polynomial.Polynomial.fit(x, y, deg, full=True)
series = polyfit[0]
resid = polyfit[1][0]
print('poly series:', series)
print('resid:', resid)
print('resid etc:', polyfit[1])

'''
import matplotlib.pyplot as plt
_ = plt.plot(x, y, 'o', label='Original data', markersize=10)
_ = plt.plot(x, m*x + c, 'r', label='Fitted line')
_ = plt.legend()
plt.show()
'''

