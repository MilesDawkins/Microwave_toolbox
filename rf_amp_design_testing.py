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
#lc,lr,min_gl= amp_calc.calc_gain_circle("load",match_gain/2,10E9)




microstrip_ref = mt.t_line_tools.microstrip(50,4.4,1.6E-3,1)
lamb = microstrip_ref.wavelength(10E9)

gs_stub_l = (1/np.atan(mt.system_tools.gamma_2_impedance(50,np.abs(min_gs))/50))/(2*np.pi) # calculating required open circuit stub length
gs_phase_l = (np.angle(1/((1/50)+(1/(-1J*50*1/np.tan(2*np.pi*gs_stub_l)))))-np.angle(min_gs))/(2*np.pi) #calculating phasing line length using differences of phase
















print("--- %s seconds ---" % (time.time() - start_time))
##################plotting functions#######################
smith = mt.plotting_tools.smith_chart()

real = np.real(amp_calc.source_max_gain_gamma)
imag = np.imag(amp_calc.source_max_gain_gamma)
smith.ax.plot(real,imag)


smith.ax.add_patch(patches.Circle((np.real(sc),np.imag(sc)), sr, edgecolor='r', facecolor='none'))


#annotate every 1GHz
point = 0
for xy in zip(real, imag):  
    if bjt.frequencies[point]%1E9 == 0:
        smith.ax.annotate('(%s)' % (bjt.frequencies[point]/1E9), xy=xy, textcoords='data') 
        smith.ax.plot(real[point],imag[point], marker='o',markersize = 2 , c='black', linestyle='none')
    point = point + 1


plot.grid()
plot.show()


