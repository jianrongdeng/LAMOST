"""
============================
script: stats.py
============================
	date: 20180522 by Jianrong Deng
	purpose:
		common tools in statistical calculation
"""


#============================
def checkDistribution(data_array, Nsigma=5, info='', verbose=1):
#============================
    """
    purpose: calculate the mean value and the sstd of the inputdata array 
    input : 
       data_array: data point (in array)
       Nsigma: default is to print out points outside 5 sigma region
       info: additional info to print out 

    output: print out a list of out of range points

    """

    import statistics as sts
    data = sorted(data_array)
 
    # mean and sstd of the mean array
    mean = sts.mean(data)
    sstd = sts.stdev(data)

    print( ' dataset : ', info)
    print( '    mean = ', mean, '    sstd = ', sstd)
    print ('    [  ', data[0], ' ,', data[1],  ' ,', data[2], '...,', ' ,', data[-3],  data[-2], ' ,', data[-1], ' ]')


    # check >5sigma points:
    delta_a = mean - Nsigma * sstd
    delta_b = mean + Nsigma * sstd

    print( '    check outside -', Nsigma, 'sigma points: ')
    # data point < ( mean -5sigma )
    for i in range(len(data)):
        if (data[i] < delta_a):
            if (verbose == 1): print ( '      data = ', data[i])
        else:
            np = i  # number of points outside the range
            print ( '      number of points outside the range = ', np )
            break

    print( '    check outside +', Nsigma, 'sigma points: ')
    data.sort(reverse=True)
    # data point < ( mean -5sigma )
    for i in range(len(data)):
        if (data[i] > delta_b):
            if (verbose == 1): print ( '      data = ', data[i])
        else:
            np = i  # number of points outside the range
            print ( '      number of points outside the range = ', np )
            break


    return
#============================

#============================
def w_cov(data_array, weight=True):
#============================
    """
    purpose: calculate the weighted covariance matrix
    input : 
       data_array: data point (in array [[x1, y1, pV1], [x2, y2, pV2], ...])
       weight: if True, use pV as weight 

    output: 
       cov: covariance matrix


    """
    import numpy as np

    # transpose matrix: [ [ x1, x2, x3...], [y1, y2, y3...], [pV1, pV2, pV3...]]
    data = np.array(data_array).T

    if weight:
        cov = np.cov(data[0], data[1], aweights=data[2])
    else:    
        cov = np.cov(data[0], data[1])
       
    return cov 
#============================

#============================
def coef(cov):
#============================
    """
    purpose: calculate the correlation coefficient from the input covariance matrix
    input : 
       cov: covariance matrix

    output: 
       coef: correlation coefficient


    """
    import numpy as np


    # now try to calculate coef from the covariance matrix
    if (cov[0, 0] == 0 or cov[1, 1] == 0 ): 
        '''
        print('cov[0,1] =', cov[0, 1])
        print('cov[0,0] =', cov[0, 0])
        print('cov[1,1] =', cov[1, 1])
        '''
        coef = 1.5 # if cov00 or cov11 = 0, set coef to a value > 1 to mark this kind of events
    else:     
        coef = cov[0,1]/np.sqrt( cov[0,0]*cov[1,1]) 
       
    return coef
#============================


#============================
def cal_corr(pixelList, weight=True) :
#============================
    """
    purpose: calculate the correlation coefficient and the eigen Values of the input pixel dataset
    input : 
       pixelList: the input dataset of the pixels 

    output: 
       coef: correlation coefficient
       eigVal: the float ndarray of the eigen values


    """
    from numpy import linalg 
    cov = w_cov(pixelList, weight=weight)
    eigVal = linalg.eigvalsh(cov)
       
    return coef(cov), eigVal
#============================



"""
def sstd
import numpy as np
import statistics as sts

mean = np.mean(data)
sstd = sts.stdev(data.flatten())
"""


"""
#============================
def w_coef(data_array, weight=True):
#============================
    '''
    purpose: calculate the weighted correlation coefficient
    input : 
       data_array: data point (in array [[x1, y1, pV1], [x2, y2, pV2], ...])
       weight: if True, use pV as weight 

    output: 
       coef: correlation coefficient


    '''
    import numpy as np

    cov = w_cov(data_array, weight)
    # now try to calculate coef from the covariance matrix
    coef = cov[0,1]/np.sqrt(cov[0,0]*cov[1,1])
       
    return coef
#============================
"""

