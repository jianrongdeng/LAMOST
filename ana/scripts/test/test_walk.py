
"""
============================
test_walk.py
============================
	date: 20180523 by Jianrong Deng
        Purpose: test the function of os.walk(topdir)

============================
"""


import os
path='/Users/jdeng/baiduCloudDisk/LAMOST/ana/outputs/run1_20171205'
for root, dirs, files in os.walk(path, topdown=True):
   print('loop through files: ') 
   for name in files:
      print(os.path.join(root, name))
   print ('loop through dirs:' )
   for name in dirs:
      print(os.path.join(root, name))
