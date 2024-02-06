# This version uses Numpy everywhere
import timeit

import numpy as np
from matplotlib import pyplot as plt
from numpy import NaN

start = timeit.default_timer()

N0 = 10000
N1 = 10000

# Shape should be 10000 x 24000 ...ignore the last row
traces0 = np.load('tvla_traces_hw3/tvla_0traces_int16.npy')
traces1 = np.load('tvla_traces_hw3/tvla_1traces_int16.npy')
# To ignore the last spurious value
tvlatraces0 = traces0[0:10000, ]
tvlatraces1 = traces1[0:10000, ]

mean0 = np.array(tvlatraces0)
mean0 = np.mean(mean0, axis=0)

mean1 = np.array(tvlatraces1)
mean1 = np.mean(mean1, axis=0)

var0 = np.array(tvlatraces0)
var0 = np.var(var0, axis=0)
var0 = var0 / N0

var1 = np.array(tvlatraces1)
var1 = np.var(var1, axis=0)
var1 = var1 / N1

numerator = mean0 - mean1
intermediate = var0 + var1
denominator = np.sqrt(intermediate)
# Avoid division by 0
numerator[np.where(denominator == 0)] = 0
denominator[np.where(denominator == 0)] = 1

tvalues = numerator / denominator

plt.ylim(-10, 10)
t_threshold = [4.5] * 24000
minus_t_threshold = [-4.5] * 24000
plt.plot(t_threshold, color='b', label="t-value upper threshold")
plt.plot(minus_t_threshold, color='b', label="t-value lower threshold")
plt.legend()

plt.xlabel("Time points")
plt.ylabel("t-value")

plt.plot(tvalues, color='r')
plt.savefig('tvalplot2')

print("Timepoints where t-value threshold has been exceeded:")
timepoints_gt = np.where(tvalues > 4.5)[0]
timepoints_lt = np.where(tvalues < -4.5)[0]
print(timepoints_gt)
print(timepoints_lt)

stop = timeit.default_timer()
print((stop - start) * 1000.0)
