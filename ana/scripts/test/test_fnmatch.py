"""
============================
test_fnmatch.py
============================
	date: 20180611 by Jianrong Deng
        Purpose: test the function of fnmatch
============================
"""

import fnmatch

#det_tag = str('rb-01r*')
det_tag = str('*01r*')
filename = 'rb-01r-20160101174212-clusters.dat'
d_tag = '*clusters.dat'


if fnmatch.fnmatch(filename, det_tag): print('det_tag = {}, filename = {}'.format(det_tag, filename) )
if fnmatch.fnmatch(filename, d_tag): print('d_tag = {}, filename = {}'.format(d_tag, filename) )


