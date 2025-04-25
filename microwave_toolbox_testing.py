import microwave_toolbox as mt
import matplotlib.pyplot as plot
import matplotlib.patches as patches
import numpy as np
import os
import time

##############setup functions####################
start_time = time.time()
script_directory = os.path.dirname(os.path.abspath(__file__))
file = os.path.join(script_directory,"BFP840FESD_VCE_2.0V_IC_22mA.s2p")

#################calulation functions###########################
freqs = np.linspace(1E9,11E9,1000)

bjt = mt.system_tools.network(file)

t_line_s = mt.t_line_tools.microstrip(50,1,1.6E-3,10E-3,freqs_in = freqs, typem= "loaded", zl_in=1000, shunt_in=True)
t_line = mt.t_line_tools.microstrip(50,1,1.6E-3,20E-3,freqs_in = freqs)

shunt_t_line_cascade = mt.system_tools.network_cascade(t_line.network,t_line_s.network)
shunt_t_line_cascade = mt.system_tools.network_cascade(shunt_t_line_cascade,t_line.network)
amp = mt.system_tools.network_cascade(bjt,shunt_t_line_cascade)

print("--- %s seconds ---" % (time.time() - start_time))


##################plotting functions#######################
plot.plot(amp.frequencies,amp.dbmag[1][0])


smith = mt.plotting_tools.smith_chart()
real = [np.real(x) for x in shunt_t_line_cascade.complex[0][0]]
imag = [np.imag(x) for x in shunt_t_line_cascade.complex[0][0]]
smith.ax.plot(real,imag)
"""
#annotate every 1GHz
point = 0
for xy in zip(real, imag):  
    if t_line.network.frequencies[point]%1E9 == 0:
        smith.ax.annotate('(%s)' % (t_line.network.frequencies[point]/1E9), xy=xy, textcoords='data') 
        smith.ax.plot(real[point],imag[point], marker='o',markersize = 2 , c='black', linestyle='none')
    point = point + 1
"""
plot.grid()
plot.show()


