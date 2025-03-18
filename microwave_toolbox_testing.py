import microwave_toolbox as mt
import matplotlib.pyplot as plot
import numpy as np
import os


file = r"C:\Users\miles\Downloads\BFP840FESD_VCE_2.0V_IC_22mA.s2p"
file = file.replace("\\", "/")
trans_s2p = mt.network.s_param(file_path=file)

file = r"C:\Users\miles\Downloads\BFP840_EDITED.s2p"
file = file.replace("\\", "/")
filter = mt.network.s_param(file_path=file)

test = mt.network.s_param_cascade(trans_s2p,filter,interp_freq_step=10E6)
plot.plot(trans_s2p.frequencies,trans_s2p.phase[0][0])
plot.grid()

ax=mt.plot.smith_chart_matplotlib.smith_chart.__init__()
ax.plot(trans_s2p.real[0][0],trans_s2p.imag[0][0])
ax.plot(test.real[0][0],test.imag[0][0])
ax.grid()
ax.set_aspect('equal')

point = 0
for xy in zip(test.real[0][0], test.imag[0][0]):  
    if point%1000 == 0:
        ax.annotate('(%s)' % (test.frequencies[point]/1E9), xy=xy, textcoords='data') 
    point = point + 1

plot.show()

