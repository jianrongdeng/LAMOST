"""
============================
script: const.py
============================
	date: 20170612 by Jianrong Deng
	purpose: define constants used in LAMOST image processing
	
"""

### image dimesion
N_b = 5 # number of biased images
N_x = 4096 # the last pixel (in x) before overscan bands
N_y = 4136 # total number of pixels in y direction
N_os = 2  # number of overscan regions
OS_Nbins = 32  # number of total x bins in overscan regions

### pixel value threshold
th_pixel = 3  # if pixel value > 3 * sstd, keep this pixel
th_cluster =5 # require at least one pixel in a cluster has a value of 5 * sstd

# test path and file
test_path_in = '/data2/rawdata'
test_path_out = '/home/jdeng/LAMOST/ana/outputs'
test_date = '20150923'
test_datatype = 'bias'
test_det = 'rb-16r-'
test_time = [
'20150923234527-10000-82496145',
'20150923234936-10000-82496149',
'20150923235345-10000-82496153',
'20150923235754-10000-82496157',
'20150924000612-10000-82496166'
]


# debug flag
DEBUG = True
DEBUG_L2 = False
