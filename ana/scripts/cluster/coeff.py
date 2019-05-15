
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


