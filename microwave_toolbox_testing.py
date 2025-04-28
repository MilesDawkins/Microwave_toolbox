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
freqs = np.linspace(10E9, 10.01E9,1000)
bjt = mt.system_tools.network(file)

f0 = 10E9
sl = 0.125
pl = 0.13
shunt_match1 = mt.t_line_tools.microstrip(50,4.4,1.6E-3,sl,freqs_in = freqs, typem="open", shunt_in=True, length_unit="lambda", center_freq = f0)
phase_match1 = mt.t_line_tools.microstrip(50,4.4,1.6E-3,pl,freqs_in = freqs, length_unit="lambda", center_freq= f0)
phase_match2 = mt.t_line_tools.microstrip(50,4.4,1.6E-3,0.001,freqs_in = freqs, typem= "loaded", zl_in = 50)
network = phase_match1.network ** shunt_match1.network ** phase_match2.network

print("--- %s seconds ---" % (time.time() - start_time))

##################plotting functions#######################

smith = mt.plotting_tools.smith_chart()
real = [np.real(x) for x in network.complex]
imag = [np.imag(x) for x in network.complex]
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


