
"""
============================
test_np_sum.py
============================
	date: 20180523 by Jianrong Deng
        Purpose: test the function of sum() of a numpy array
============================
"""


import numpy as np

ndet = 32

N_file = np.zeros((32), dtype=int)

for i in range(0, ndet):
   N_file[i] = N_file[i] + 1

print ('total number of files = ', N_file.sum())
for i in range(0, ndet):
    print ( (int(i + 1)), ": \t", N_file[i])



