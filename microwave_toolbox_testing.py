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
freqs = np.linspace(1, 2E9,1000)
bjt = mt.system_tools.network(file)

microstrip_ref = mt.t_line_tools.microstrip(50,4.4,1.6E-3,1)
print(microstrip_ref.ereff)
lamb = microstrip_ref.wavelength(950E6)

sl = 0.125*lamb
pl = 0.125*lamb

z1 = 100
z2 = 25
z12 = 100


shunt_match1 = mt.t_line_tools.microstrip(z1,4.4,1.6E-3,sl,freqs_in = freqs, typem="open", shunt_in=True)
shunt_match2 = mt.t_line_tools.microstrip(z2,4.4,1.6E-3,sl,freqs_in = freqs, typem="open", shunt_in=True)
shunt_match3 = mt.t_line_tools.microstrip(z1,4.4,1.6E-3,sl,freqs_in = freqs, typem="open", shunt_in=True)

phase_match1 = mt.t_line_tools.microstrip(z12,4.4,1.6E-3,pl,freqs_in = freqs)
phase_match2 = mt.t_line_tools.microstrip(z12,4.4,1.6E-3,pl,freqs_in = freqs)



network = (shunt_match1.network ** phase_match1.network) ** shunt_match2.network ** phase_match2.network



print("--- %s seconds ---" % (time.time() - start_time))


##################plotting functions#######################
plot.plot(network.frequencies,network.linmag[1][0])


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


