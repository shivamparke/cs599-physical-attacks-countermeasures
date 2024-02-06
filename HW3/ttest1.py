# This version uses naive approach
import math
import timeit

import numpy as np
from matplotlib import pyplot as plt

start = timeit.default_timer()

N0 = 10000
N1 = 10000

# Shape should be 10000 x 24000 ...ignore the last row
traces0 = np.load('tvla_traces_hw3/tvla_0traces_int16.npy')
traces1 = np.load('tvla_traces_hw3/tvla_1traces_int16.npy')
# To ignore the last spurious value
tvlatraces0 = traces0[0:10000, ]
tvlatraces1 = traces1[0:10000, ]

tvals = np.zeros(24000)

for i in range(24000):
    mean0 = np.mean(tvlatraces0[:, i])
    mean1 = np.mean(tvlatraces1[:, i])

    s0 = np.var(tvlatraces0[:, i])
    s1 = np.var(tvlatraces1[:, i])

    numerator = mean0 - mean1
    intermediate = (s0 / N0) + (s1 / N1)
    denominator = math.sqrt(intermediate)
    if denominator == 0:
        continue
    tvalue = numerator / denominator
    tvals[i] = tvalue
    if tvalue > 4.5 or tvalue < -4.5:
        print("t-value threshold exceeded for timepoint:", i)

t_threshold = [4.5] * 24000
minus_t_threshold = [-4.5] * 24000
plt.plot(t_threshold, color='b')
plt.plot(minus_t_threshold, color='b')

plt.xlabel("Time points")
plt.ylabel("t-value")

plt.plot(tvals, color='r')
plt.savefig('tvalplot')

stop = timeit.default_timer()
print((stop - start) * 1000.0)
