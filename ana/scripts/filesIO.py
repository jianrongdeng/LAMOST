"""
============================
script: filesIO.py
============================
	date: 20170615 by Jianrong Deng
	purpose:
		handle input / output files
	Input: input dir, date, time 
"""

import const

#==========================
def getFilename (path=const.test_path_out, date=const.test_date, datatype=const.test_datatype, det=const.test_det, time=const.test_time[0], tag = '-sub_overscan-sub_bias', postfix = '.fit'): 
    """
    purpose: name scheme for net data (= raw - overscan - bias) file
    """
    filename =  path + date + datatype + det + time + tag + postfix
    return filename

#==========================
def getMaskFilename(path=const.test_path_out, date=const.test_date, datatype=const.test_datatype, det=const.test_det, time=const.test_time[0], tag = '-3sigma_mask', postfix = '.fit'): 
    """
    purpose: name scheme for 3sigma-mask file
    """
    filename =  path + date + datatype + det + time + tag + postfix
    return filename

#==========================
def getClusterFilename(path=const.test_path_out, date=const.test_date, datatype=const.test_datatype, det=const.test_det, time=const.test_time[0], tag = '-cluster', postfix = '.txt'): 
    """
    purpose: name scheme for 3sigma-mask file
    """
    filename =  path + date + datatype + det + time + tag + postfix
    return filename



