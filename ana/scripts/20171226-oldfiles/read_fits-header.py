"""
=======================================
Read header from a FITS file
=======================================

*By: Jianrong Deng 20170517 
-------------------

"""

##############################################################################
# load the FITS files used by this script:

from astropy.io import fits
image_file = '/Users/jdeng/baiduCloudDisk/LAMOST/data/20150923/bias/rb-16r-20150924000612-10000-82496166.fit.gz'
hdulist = fits.open(image_file)

##############################################################################
# Use `astropy.io.fits.info()` to display the structure of the file:
#fits.info(image_file)

hdulist.info()


image_header = fits.getheader(image_file)
#image_header = fits.getheader(image_file, ext = 0)
#image_header['HISTORY']
#image_header['COMMENT']
print(repr(image_header))

##############################################################################
# To get a list of all keywords, use the Header.keys() method just as
# you would with a dict:
# image_header.keys()

#prihdr = hdulist[0].header
#prihdr.keys()

##############################################################################
# After you are done with the opened file, close it with the HDUList.close() method:

hdulist.close()
