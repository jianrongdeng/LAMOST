"""
============================
test_filename.py
============================
	date: 20170814 by Jianrong Deng
	purpose: test fileIO functions and filename_rawdata class
============================
"""

import os
import const
import filesIO as fIO

DEBUG=const.DEBUG

#set input / output files using environment variables, create output directory if not already exist
rawfiles = fIO.get_rawfilenames()
# output file for saving pixel lists (one file for 5 lists)
file_pixelList = fIO.setOutFilename(rawfiles[0], d_tag='pixelList') 
# mean and sstd output file
file_stat = fIO.setOutFilename(rawfiles[0], d_tag='stat')
if DEBUG:
    print('rawdata files :', rawfiles)
    print('file_stat     :', file_stat)
    print('file_pixelList:', file_pixelList)
