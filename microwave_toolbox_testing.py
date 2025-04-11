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
freq = 10E9
desired_gain = 15

trans_s2p = mt.system_tools.network(file_path=file)
t_line = mt.t_line_tools.microstrip(50,4.4,1.6E-3, type = "open")
t_line.create_network(trans_s2p.frequencies,0.005)
t_line_2 = mt.t_line_tools.microstrip(50,4.4,1.6E-3)
t_line_2.create_network(trans_s2p.frequencies,0.1)
amp_w_line = mt.system_tools.network_cascade(t_line_2.network,trans_s2p)
t_cascade = mt.system_tools.network_cascade(t_line_2.network,t_line.network)
amp = mt.circuit_tools.rf_amplifier(amp_w_line)

source,load = amp.calc_transducer_impedance(freq)
trans_gain = 10*np.log10(np.interp(freq,amp.frequencies,amp.max_z0_transducer_gain))
sl_gain_needed = (desired_gain - trans_gain)/2
sc,sr,lc,lr,min_gs,min_gl = amp.calc_gain_circle(sl_gain_needed,freq)
xl,yl = np.real(lc),np.imag(lc)
xs,ys = np.real(sc),np.imag(sc)

print(trans_gain)
print(10*np.log10(np.interp(freq,amp.frequencies,amp.g_s_max_gain)))
print(10*np.log10(np.interp(freq,amp.frequencies,amp.g_l_max_gain)))
print(trans_gain+2*sl_gain_needed)
print("--- %s seconds ---" % (time.time() - start_time))




##################plotting functions#######################
smith = mt.plotting_tools.smith_chart()
real = [np.real(x) for x in amp_w_line.complex[0][0]]
imag = [np.imag(x) for x in amp_w_line.complex[0][0]]
real2 = [np.real(x) for x in t_cascade.complex[0][0]]
imag2 = [np.imag(x) for x in t_cascade.complex[0][0]]
#smith.ax.plot(real,imag)
smith.ax.plot(real2,imag2)

"""
    #annotate every 1GHz
point = 0
for xy in zip(real, imag):  
    if amp.frequencies[point]%1E9 == 0:
        smith.ax.annotate('(%s)' % (amp.frequencies[point]/1E9), xy=xy, textcoords='data') 
        smith.ax.plot(real2[point],imag2[point], marker='o',markersize = 2 , c='black', linestyle='none')
    point = point + 1
"""
smith.ax.add_patch(patches.Circle((xs,ys),sr, edgecolor='r', facecolor='none'))
smith.ax.add_patch(patches.Circle((xl,yl),lr, edgecolor='r', facecolor='none'))
smith.ax.plot(np.real(min_gs),np.imag(min_gs), marker='o', linestyle='none')
smith.ax.plot(np.real(min_gl),np.imag(min_gl), marker='o', linestyle='none')
plot.grid()



fig2, ay = plot.subplots()
ay.plot(t_cascade.frequencies,t_cascade.dbmag[0][0])
plot.grid()
plot.show()


