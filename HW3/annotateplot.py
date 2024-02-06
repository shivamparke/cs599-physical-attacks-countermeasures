import numpy as np
import holoviews as hv
from bokeh.plotting import show

plaintexts = np.load('traces_attack_hw3/textin_attack.npy')
traces = np.load('traces_attack_hw3/traces_attack_int16.npy')
testtrace = np.zeros(24000)

# As per the example on Teams
# Only for first keybyte
pltext = 0
for timepoint in range(24000):
    tracesbytime = traces[:, timepoint]
    rows_to_consider = np.where(plaintexts[:, 0] == pltext)[0]
    meanval = np.mean(tracesbytime[rows_to_consider])
    testtrace[timepoint] = meanval
    print(timepoint, "DONE")

hv.extension('bokeh')
plotwa = hv.Curve(testtrace).opts(width=900,height=900,xlim=(0, 24000), ylim=(-600, 512),xlabel="Time", ylabel="Traces")
show(hv.render(plotwa))