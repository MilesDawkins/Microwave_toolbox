import microwave_toolbox as mt
import matplotlib.pyplot as plot
import numpy as np
import os
import time

start_time = time.time()

script_directory = os.path.dirname(os.path.abspath(__file__))
file = os.path.join(script_directory,"BFP840FESD_VCE_2.0V_IC_22mA.s2p")
print(mt.antenna_tools.fspl_calc(8E9,8,dist_units = "feet"))
trans_s2p = mt.system_tools.network(file_path=file)
#mt.system_tools.reverse_network(trans_s2p)
amp = mt.circuit_tools.rf_amplifier(trans_s2p)
ax = mt.plotting_tools.smith_chart.__init__()
real = [np.real(x) for x in amp.gamma_s_max_gain]
imag = [np.imag(x) for x in amp.gamma_s_max_gain]
ax.plot(real,imag)
plot.grid()

point = 0
for xy in zip(real, imag):  
    if amp.frequencies[point]%1E9 == 0:
        ax.annotate('(%s)' % (amp.frequencies[point]/1E9), xy=xy, textcoords='data') 
    point = point + 1
print("--- %s seconds ---" % (time.time() - start_time))
plot.show()

