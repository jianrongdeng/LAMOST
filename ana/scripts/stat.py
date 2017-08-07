
def sstd
import numpy as np
import statistics as sts

mean = np.mean(data)
sstd = sts.stdev(data.flatten())
