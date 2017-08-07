"""
============================
script: read_fits.py
============================
	date: 20170606 by Jianrong Deng
"""

def read_fits (filename):
   """
	purpose:
		read in fits files
	Input: fits filename
	Output: image ndarray
   """
   from astropy.io import fits
   return fits.getdata(filename, ext=0)
   


