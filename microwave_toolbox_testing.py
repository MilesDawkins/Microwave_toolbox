import microwave_toolbox as mt
import matplotlib.pyplot as plot
import numpy as np
import os


file = r"C:\Users\miles.dawkins\Downloads\BFP840FESD_VCE_2.0V_IC_22mA.s2p"
file = file.replace("\\", "/")
trans_s2p = mt.network.s_param(file_path=file)


file = r"C:\Users\miles.dawkins\Downloads\ABF-3R3G+_Plus25degC.s2p"
file = file.replace("\\", "/")
filter = mt.network.s_param(file_path=file)

test = mt.network.s_param_cascade(trans_s2p,filter)
print(trans_s2p.frequencies)
plot.plot(test.frequencies,test.dbmag[1][0])
plot.grid()

ax=mt.plot.smith_chart_matplotlib.smith_chart.__init__()
ax.plot(trans_s2p.real[0][0],trans_s2p.imag[0][0])
ax.plot(test.real[0][0],test.imag[0][0])
ax.grid()
ax.set_aspect('equal')

point = 0
for xy in zip(trans_s2p.real[0][0], trans_s2p.imag[0][0]):  
    if point%10 == 0:
        ax.annotate('(%s)' % (trans_s2p.frequencies[point]/1E9), xy=xy, textcoords='data') 
    point = point + 1

plot.show()

