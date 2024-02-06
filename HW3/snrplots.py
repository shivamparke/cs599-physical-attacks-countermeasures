import numpy as np
from matplotlib import pyplot as plt
from numpy import float32

plaintexts = np.load('traces_attack_hw3/textin_attack.npy')
traces = np.load('traces_attack_hw3/traces_attack_int16.npy')

# Will be used to calculate variance
means_list = np.zeros((256, 24000), dtype='float')
# Will be used to calculate mean
variances_list = np.zeros((256, 24000), dtype='float')

snrarray = np.zeros(24000)

for keybyte in range(16):
    plt.figure()
    plaintexts_bycol = plaintexts[:,keybyte]  # first keybyte
    for timepoint in range(24000):
        traces_by_time = traces[:, timepoint]
        for pltext in range(256):
            # Only those traces where plaintext is same
            #traces_to_consider = traces_by_time[rows_to_consider]
            traces_to_consider = traces_by_time[np.where(plaintexts_bycol == pltext)[0]]
            mean_of_pltext = np.mean(traces_to_consider)
            means_list[pltext][timepoint] = mean_of_pltext
            var_of_pltext = np.var(traces_to_consider)
            variances_list[pltext][timepoint] = var_of_pltext

        means_to_consider = means_list[:, timepoint]
        vars_to_consider = variances_list[:, timepoint]
        # To account for 0 values:
        means_to_consider = means_to_consider[means_to_consider != 0]

        signal = np.var(means_to_consider)
        noise = np.mean(vars_to_consider)
        # So that NaN values aren't present
        if noise == 0:
            snrarray[timepoint] = 0
        else:
            snrarray[timepoint] = signal / noise


    plt.xlabel("Time")
    plt.ylabel("SNR Values")

    plt.plot(snrarray, color='b')
    plt.savefig('snr' + str(keybyte))
    print(np.argmax(snrarray))  # Timepoint of highest SNR - 1
