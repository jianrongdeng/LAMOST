"""
============================
test_matplotlib.py
============================
	date: 20180527 by Jianrong Deng
        Purpose: test the 2D scatter plot in the matplotlib module. 
	   Will use the 2D bitmap to check the cluster algerithm
	   graphically.
============================
"""

import matplotlib.pyplot as plt


fig = plt.figure()

x = range(10)
y = range(10, 20)

plt.plot(x, y, 'r*')

plt.axis([0, 10,  10, 20])
plt.show()

