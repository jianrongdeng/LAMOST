"""
============================
test_covariance.py
============================
	date: 20190305 by Jianrong Deng
        Purpose: test covariance calculate of a 2-D matrix
	Method: use the function gaussian_kdefrom scipy import stats
	Input: 2-D (x, y) datasets
	Output: Covariance matrix
                Pearson's corralation coefficient
        Reference: https://en.wikipedia.org/wiki/Pearson_correlation_coefficient        
               https://docs.scipy.org/doc/numpy/reference/generated/numpy.corrcoef.html#numpy.corrcoef
               https://pythonfordatascience.org/variance-covariance-correlation/
        example1: 
            data = stats.gaussian_kde(pixels)
            print ( data.covariance)
============================
"""
#============================
def w_coef(data_array, weight=True):
#============================
    """
    purpose: calculate the correlation coefficient
    input : 
       data_array: data point (in array [[x1, y1, pV1], [x2, y2, pV2], ...])
       weight: if True, use pV as weight 

    output: 
       coef: correlation coefficient


    """
    import numpy as np

    # transpose matrix: [ [ x1, x2, x3...], [y1, y2, y3...], [pV1, pV2, pV3...]]
    data = np.array(data_array).T
    #print('data_array[0]=', data_array[0])
    #print('data_array[1]=', data_array[1])
    #print('data_array[2]=', data_array[2])
    #print('data[0]_T=', data[0])
    #print('data[1]_T=', data[1])
    #print('data[2]_T=', data[2])

    if weight:
        cov = np.cov(data[0], data[1], aweights=data[2])
    else:    
        cov = np.cov(data[0], data[1])
    #print('covariance =\n', cov)
    # now try to calculate coef from the covariance matrix
    coef = cov[0,1]/np.sqrt(cov[0,0]*cov[1,1])
    #print('correlation coefficient using weighted covariance matrix=', coef)


    # use the X and Y vectors
    # coef_VXY = np.corrcoef([data[0], data[1]])[0, 1]
    # print('correlation coefficient_Vxy=', coef_VXY)
       
    return coef
#============================



import numpy as np
#from scipy import stats

# note: the input format should be data = [[x1, x2, x3... ], [y1, y2, # y3...]
# therefore use np.array(pixels).T, the transpose matrix
#pixels = [ [4133, 1394], [4134, 1393], [4135, 1392]]
pixels = [ [4133, 394, 3000], [4134, 1393, 5000], [4135, -2392, 2000]]
pixels_T = np.array(pixels  ).T

print('pixels = \n',pixels)

# covariance
cov = np.cov(pixels_T)
print('covariance =\n', cov)


# covariance
cov_XY = np.cov(pixels_T[0], pixels_T[1], aweights=pixels_T[2])
print('weighted covariance_XY =\n', cov_XY)

# the correlation coefficient
coef = np.corrcoef(pixels_T)
print('correlation coefficient = \n', coef)
print('correlation coefficient_xy=', coef[0, 1])

# use the X and Y vectors
coef_VXY = np.corrcoef([pixels_T[0], pixels_T[1]])[0, 1]
print('correlation coefficient_Vxy=', coef_VXY)

# now try to calculate coef from the covariance matrix
coef_cov = cov[0,1]/np.sqrt(cov[0,0]*cov[1,1])
print('correlation coefficient using covariance matrix=', coef_cov)

# now try weighted covariance 
cov_w = np.cov(pixels_T, aweights=pixels_T[2])
print('weighted covariance =\n', cov_w)
coef_cov_w = cov_w[0,1]/np.sqrt(cov_w[0,0]*cov_w[1,1])
print('correlation coefficient using weighted covariance matrix=', coef_cov_w)


coef_stat = w_coef(pixels)
print('from function corrcoef: correlation coefficient using weighted covariance matrix=', coef_stat)


