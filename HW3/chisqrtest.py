import math
import numpy as np
import scipy.stats
from matplotlib import pyplot as plt

traces0 = np.load('tvla_traces_hw3/tvla_0traces_int16.npy')
traces1 = np.load('tvla_traces_hw3/tvla_1traces_int16.npy')

# Shape should be 10000 x 24000 ...ignore the last row
# To ignore the last spurious value:
tvlatraces0 = traces0[0:10000, ]
tvlatraces1 = traces1[0:10000, ]

# TEST VALUES:
'''
myarr1 = np.array([-3 for x in range(3)])
myarr2 = np.array([-1 for y in range(2)])
myarr3 = np.array([1 for z in range(6)])
array0 = np.concatenate((myarr1, myarr2, myarr3))
# print(array0)

myarr1 = np.array([2 for a in range(4)])
myarr2 = np.array([1 for b in range(2)])
myarr3 = np.array([5 for c in range(5)])
array1 = np.concatenate((myarr1, myarr2, myarr3))
# print(array1)
'''

pvals = np.zeros(24000)

for timepoint in range(24000):
    # Instead of array0 and array1, use tvlatraces0 and tvlatraces1
    array0 = tvlatraces0[:, timepoint]
    array1 = tvlatraces1[:, timepoint]

    # Sorted order
    values0, frequencies0 = np.unique(array0, return_counts=True)
    values1, frequencies1 = np.unique(array1, return_counts=True)

    # print(values0, frequencies0)
    # print(values1, frequencies1)

    # Concatenate arr0 and arr1, NOT vals0 and vals1
    combined = np.concatenate((array0, array1))
    uniq_vals, colcount = np.unique(combined, return_counts=True)
    # print(uniq_vals, colcount)

    # uniq_vals has the unique bins, its size - 1 = dof
    dof = uniq_vals.size - 1
    # print(dof)

    # For bins that are common in i = 0, and i = 1, we need to know the value to be subtracted from Eij value
    # For bins that are unique (i.e., only in i = 0, or in i = 1), we can simply do 2 * Eij
    deltaarray = np.zeros(uniq_vals.size, dtype=int)
    # print(deltaarray)

    # Intersection way of doing things
    # values0/1, frequencies0/1 => DON'T MESS UP!
    common_bins = np.intersect1d(values0, values1)
    for cbin in common_bins:
        index_uniqvals = np.where(uniq_vals == cbin)
        index_vals = np.where(values0 == cbin)
        deltaarray[index_uniqvals] = frequencies0[index_vals]

    # print(deltaarray)
    # print(colcount)

    exp_frequencies = colcount / 2
    # print(exp_frequencies)

    chisqr_darray = 2 * (((exp_frequencies - deltaarray) ** 2) / exp_frequencies)
    chisqrd_sum = np.sum(chisqr_darray)
    # print(chisqrd_sum)

    result = scipy.stats.chi2.sf(chisqrd_sum, dof)
    # result2 = 1 - scipy.stats.chi2.cdf(chisqrd_sum, dof)
    if math.isnan(result):
        pvals[timepoint] = 1
        continue
    pvals[timepoint] = result

    if result <= 0.00001:
        print("p-value threshold exceeded for timepoint:", timepoint)

'''
Final plotting code:
'''
plt.ylim(10**-7, 1)
p_threshold = [0.00001] * 24000
plt.semilogy(p_threshold, color='black', label="p-value threshold")
plt.legend()
plt.xlabel("Time points")
plt.ylabel("p-value")
plt.semilogy(pvals, color='r')
plt.savefig('chisqrdplot2')
