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
freqs = np.linspace(1E9,12E9,1000)

bjt = mt.system_tools.network(file)

microstrip_ref = mt.t_line_tools.microstrip(50,4.4,1.6E-3,1)
lamb = microstrip_ref.wavelength(3E9)


shunt_match = mt.t_line_tools.microstrip(50,4.4,1.6E-3,0.15*lamb,freqs_in = freqs, typem="short", shunt_in=True)
phase_match = mt.t_line_tools.microstrip(50,4.4,1.6E-3,0.116*lamb,freqs_in = freqs, typem="loaded",zl_in=115)
match = mt.system_tools.network_cascade(shunt_match.network,phase_match.network)


print("--- %s seconds ---" % (time.time() - start_time))


##################plotting functions#######################
plot.plot(match.frequencies,match.dbmag)

"""
smith = mt.plotting_tools.smith_chart()
real = [np.real(x) for x in shunt_t_line_cascade.complex[0][0]]
imag = [np.imag(x) for x in shunt_t_line_cascade.complex[0][0]]
smith.ax.plot(real,imag)

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


