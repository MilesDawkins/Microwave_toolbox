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
freqs = np.linspace(1E1,12E9,1000)
gain_req = 16.78724978143363

bjt = mt.system_tools.network(file)

amp_calc = mt.circuit_tools.rf_amplifier(bjt)

trans_gain = 10*np.log10(np.interp(10E9,amp_calc.frequencies,amp_calc.max_transducer_gain))
print(trans_gain)

source_max_gain = 10*np.log10(np.interp(10E9,amp_calc.frequencies,amp_calc.source_max_gain))
print(source_max_gain)

sc,sr,min_gs= amp_calc.calc_gain_circle("source",source_max_gain-0.05,10E9)





microstrip_ref = mt.t_line_tools.microstrip(50,4.4,1.6E-3,1)
lamb = microstrip_ref.wavelength(10E9)

gs_stub_l = (1/np.atan(mt.system_tools.gamma_2_impedance(50,np.abs(min_gs))/50))/(2*np.pi) # calculating required open circuit stub length
gs_phase_l = (np.angle(1/((1/50)+(1/(-1J*50*1/np.tan(2*np.pi*gs_stub_l)))))-np.angle(min_gs))/(2*np.pi) #calculating phasing line length using differences of phase


shunt_source = mt.t_line_tools.microstrip(50,4.4,1.6E-3,gs_stub_l,freqs_in = freqs, typem="short", shunt_in=True, length_unit="lambda", center_freq = 10E9)
phase_source = mt.t_line_tools.microstrip(50,4.4,1.6E-3,gs_phase_l,freqs_in = freqs, length_unit="lambda", center_freq= 10E9)













print("--- %s seconds ---" % (time.time() - start_time))
##################plotting functions#######################
smith = mt.plotting_tools.smith_chart()

smith.plot_complex(amp_calc.source_max_gain_gamma)
smith.plot_circle(sc,sr)




#annotate every 1GHz
"""
point = 0
for xy in zip(real, imag):  
    if bjt.frequencies[point]%1E9 == 0:
        smith.ax.annotate('(%s)' % (bjt.frequencies[point]/1E9), xy=xy, textcoords='data') 
        smith.ax.plot(real[point],imag[point], marker='o',markersize = 2 , c='black', linestyle='none')
    point = point + 1
"""

plot.grid()
plot.show()


