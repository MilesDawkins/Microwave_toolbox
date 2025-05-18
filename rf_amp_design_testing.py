import microwave_toolbox as mt
import matplotlib.pyplot as plot
import matplotlib.patches as patches
import numpy as np
import os
import time

##############setup functions####################
start_time = time.time()
script_directory = os.path.dirname(os.path.abspath(__file__))
file = os.path.join(script_directory,"BFP840ESD_VCE_2.0V_IC_22mA.s2p")

#################calulation functions###########################
freqs = np.linspace(1E1,12E9,1000)
gain_req = 16.78724978143363
fo= 3E9

bjt = mt.system_tools.network(file)
amp_calc = mt.circuit_tools.rf_amplifier(bjt)
microstrip_ref = mt.t_line_tools.microstrip(50,4.4,1.6E-3,1)
lamb = microstrip_ref.wavelength(fo)

max_gain = 10*np.log10(np.interp(fo,amp_calc.frequencies,amp_calc.max_transducer_gain))
print(max_gain)

att = mt.circuit_tools.attenuator(50,3,config = "pi",freqs_in = freqs)

source_max_gain = 10*np.log10(np.interp(fo,amp_calc.frequencies,amp_calc.source_max_gain))
print(source_max_gain)

sc,sr,min_gs= amp_calc.calc_gain_circle("source",source_max_gain-0.05,fo)

gs_stub_l = -1*(1/np.atan2(mt.system_tools.gamma_2_impedance(50,np.abs(min_gs)),50))/(2*np.pi)+0.51 # calculating required open circuit stub length
gs_phase_l = (np.angle(1/((1/50)+(1/(-1J*50*1/np.tan(2*np.pi*gs_stub_l)))))-np.angle(min_gs))/(2*np.pi)+0.01 #calculating phasing line length using differences of phase


shunt_source = mt.t_line_tools.microstrip(50,4.4,1.6E-3,gs_stub_l,freqs_in = freqs, typem="open", shunt_in=True, length_unit="lambda", center_freq = fo)
phase_source = mt.t_line_tools.microstrip(50,4.4,1.6E-3,gs_phase_l+0.5,freqs_in = freqs, length_unit="lambda", center_freq= fo)


print(gs_stub_l*lamb)
print(gs_phase_l*lamb+0.5*lamb)


source_match = shunt_source.network**phase_source.network

amp = source_match ** bjt ** att.network







print("--- %s seconds ---" % (time.time() - start_time))
##################plotting functions#######################
#plot.plot(amp_calc.frequencies,10*np.log10(amp_calc.max_transducer_gain))
plot.plot(amp.frequencies,amp.dbmag[1,1])
plot.plot(amp.frequencies,amp.dbmag[0,0])
plot.plot(amp.frequencies,amp.dbmag[1,0])
plot.plot(amp.frequencies,amp.dbmag[0,1])
plot.legend(["s22","s11","s21","s12"])
plot.grid()

smith = mt.plotting_tools.smith_chart()
smith.plot_complex(amp_calc.source_max_gain_gamma[0:int(len(amp_calc.source_max_gain_gamma))])
smith.plot_complex(source_match.complex[1,1,0:int(len(source_match.complex[1,1])/2)])
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


