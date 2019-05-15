"""
=======================================
script: outlier_Grubbs_test_onesided_max.py
=======================================

*By: Jianrong Deng 20170531
Purpose: Grubbs' Test for Outliers
Reference: http://www.itl.nist.gov/div898/handbook/eda/section3/eda35h1.htm
Input: 
	data set
	Significance Level
Output: 
	True: there are no outliers in the data set
	False: there is exactly one outlier in the data set
-------------------
"""

import statistics as sts
import math
from scipy.stats import t
from scipy.stats import norm

y = [-2, 0, 18343, 2, 0 ] 
n_s = 7             # number of sigma away from center y = 0
cdf = norm.cdf(n_s) # cumulative distribution function at y = n_s
Prob = 2 * cdf - 1 # probability of abs( y - y_mean) <= n_s * stdev

#a = 1 - 0.6827   # Significance Level (SL)  -- 1 sigma
#a = 1 - 0.999999998027   # Significance Level (SL) -- 6sigma
a = 2 * (1 - cdf)  # SL = 1 - Prob 
print (' n_sigma = \t', n_s)
print (' probability = ', Prob)
print (' Significance Level = ', a)

N = len(y) # Degree Of Freedom (DOF)
y_max = max(y)
y_mean = sts.mean(y)
y_sstd = sts.stdev(y) # sample standard deviation
print ('mean = ', y_mean)
print ('sample standard deviation = ', y_sstd)
G = (y_max - y_mean)  / y_sstd

rv = t(N - 2)   # t distribution with N-2 DOF
T = rv.isf(a/N) # critical value of t distribution with N-2 DOF and a SL of a/N
G_c = (N - 1) / math.sqrt(N) * math.sqrt(T**2 / ((N-2) + T**2))
print ('G = ', G)
print ('G_c = ', G_c)

if G > G_c :
   print ('no outliers is rejected at the significance level of ', a)
else:
   print ('the maximum value is in fact an outlier at the significance level of ', a)


