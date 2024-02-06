import numpy as np
from numpy import float32

plaintexts = np.fromfile('plaintext_10000x16_uint8.bin', dtype='uint8')
plaintexts = np.reshape(plaintexts, (10000, 16))
traces = np.fromfile('traces_10000x50_int8.bin', dtype='int8')
traces = np.reshape(traces, (10000, 50))

# Will be used to calculate variance
means_list = np.zeros((256, 50), dtype=float32)
# Will be used to calculate mean
variances_list = np.zeros((256, 50), dtype=float32)

# for keybyte in range(16) if needed for all bytes
for timepoint in range(50):
    for pltext in range(256):
        # Total occurences of the plaintext byte in consideration
        # occurences = np.count_nonzero(plaintexts[:,0] == pltext)
        # SNR for only first byte is being considered
        # All such rows where you will find plaintext under consideration in the (timepoint)th column of traces
        rows_to_consider = np.where(plaintexts[:, 0] == pltext)[0]
        if rows_to_consider.size == 0:
            # print("NAN FOUND for timepoint ", timepoint, "and plaintext ", pltext)
            # 255 doesn't exist in the plaintexts data
            continue
        # To compute vertically
        traces_by_time = traces[:, timepoint]
        # Only those traces where plaintext is same
        traces_to_consider = traces_by_time[rows_to_consider]
        mean_of_pltext = np.mean(traces_to_consider)
        means_list[pltext][timepoint] = mean_of_pltext
        var_of_pltext = np.var(traces_to_consider)
        variances_list[pltext][timepoint] = var_of_pltext

    means_to_consider = means_list[:, timepoint]
    vars_to_consider = variances_list[:, timepoint]
    signal = np.var(means_to_consider)
    noise = np.mean(vars_to_consider)
    snr = signal / noise
    with open('signal.txt', 'a') as sigfile, open('noise.txt', 'a') as noisfile, open('snr.txt', 'a') as snrfile:
        sigfile.write(str(signal) + '\n')
        noisfile.write(str(noise) + '\n')
        snrfile.write(str(snr) + '\n')

