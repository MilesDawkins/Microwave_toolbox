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
gain_req = 6

bjt = mt.system_tools.network(file)
amp_calc = mt.circuit_tools.rf_amplifier(bjt)

trans_gain = 10*np.log10(np.interp(10E9,amp_calc.frequencies,amp_calc.max_transducer_gain))
match_gain = gain_req - trans_gain
sc,sr,lc,lr, min_gs, min_gl = amp_calc.calc_gain_circle(match_gain/2,10E9)
totalgain = trans_gain + match_gain
print(trans_gain)
print(totalgain)
print(min_gs)
print(min_gl)

microstrip_ref = mt.t_line_tools.microstrip(50,4.4,1.6E-3,1)
lamb = microstrip_ref.wavelength(10E9)
print(lamb)

#6db amp sim
phase_source =  mt.t_line_tools.microstrip(50,4.4,1.6E-3,0.165*lamb,freqs_in = freqs)
shunt_source = mt.t_line_tools.microstrip(50,4.4,1.6E-3,0.11*lamb,freqs_in = freqs, typem="open", shunt_in=True)
phase_load =  mt.t_line_tools.microstrip(50,4.4,1.6E-3,0.167*lamb,freqs_in = freqs)
shunt_load = mt.t_line_tools.microstrip(50,4.4,1.6E-3,0.162*lamb,freqs_in = freqs, typem="open", shunt_in=True)
source_match = mt.system_tools.network_cascade(shunt_source.network,phase_source.network)
load_match = mt.system_tools.network_cascade(phase_load.network,shunt_load.network)

amp = mt.system_tools.network_cascade(source_match,bjt)
amp_total = mt.system_tools.network_cascade(amp,load_match)

print("--- %s seconds ---" % (time.time() - start_time))


##################plotting functions#######################
plot.plot(amp_total.frequencies,amp_total.dbmag[0][0])

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


