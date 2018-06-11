"""
============================
script: stat.py
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

"""
def sstd
import numpy as np
import statistics as sts

mean = np.mean(data)
sstd = sts.stdev(data.flatten())
"""


