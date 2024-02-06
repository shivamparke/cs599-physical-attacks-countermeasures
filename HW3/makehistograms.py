import numpy as np
from matplotlib import pyplot as plt
from numpy import float32, uint8
import holoviews as hv
from bokeh.plotting import show
plt.style.use('seaborn-deep')

plaintexts = np.load('traces_attack_hw3/textin_attack.npy')
traces = np.load('traces_attack_hw3/traces_attack_int16.npy')

# For key byte 0, SNR is at 1372 (0-based indexing)
# Calculated and saved from snrplots.py code
snr_indices = [1372, 2798, 1500, 1564, 1628, 1692, 3294, 1820, 1884, 1948, 2012, 3790, 2140, 2204, 2268, 66]
intermediate_array = plaintexts[:, 1]
intermediate_array = np.unpackbits(intermediate_array.astype(uint8))
hamming_weights_arr = np.sum(intermediate_array.reshape(20000, 8), axis=1)
for keybyte in range(16):
    plt.figure()
    for hw in range(9):
        rows_to_consider = np.where(hamming_weights_arr == hw)[0]
        traces_to_consider = traces[:, snr_indices[keybyte]]
        traces_to_consider = traces_to_consider[rows_to_consider]
        bins = np.linspace(np.min(traces_to_consider), np.max(traces_to_consider))
        plt.hist(traces_to_consider, bins, label=str(hw))
        plt.legend(loc='best')
    plt.savefig('histogram' + str(keybyte))