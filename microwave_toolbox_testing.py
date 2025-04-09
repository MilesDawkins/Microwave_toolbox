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
t_line = mt.t_line_tools.microstrip(50,4.4,1.6E-3)
t_line.create_network(trans_s2p.frequencies,0.1)
amp_w_line = mt.system_tools.network_cascade(t_line.network,trans_s2p)
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
print((50*((-1-min_gs)/(min_gs-1))))
print((50*((-1-min_gl)/(min_gl-1))))
print(trans_gain+2*sl_gain_needed)
print("--- %s seconds ---" % (time.time() - start_time))




##################plotting functions#######################
smith = mt.plotting_tools.smith_chart()
real = [np.real(x) for x in amp.transistor.complex[1][1]]
imag = [np.imag(x) for x in amp.transistor.complex[1][1]]
smith.ax.plot(real,imag)
    #annotate every 1GHz
point = 0
for xy in zip(real, imag):  
    if amp.frequencies[point]%1E9 == 0:
        smith.ax.annotate('(%s)' % (amp.frequencies[point]/1E9), xy=xy, textcoords='data') 
        smith.ax.plot(real[point],imag[point], marker='o',markersize = 2 , c='black', linestyle='none')
    point = point + 1
smith.ax.add_patch(patches.Circle((xs,ys),sr, edgecolor='r', facecolor='none'))
smith.ax.add_patch(patches.Circle((xl,yl),lr, edgecolor='r', facecolor='none'))
smith.ax.plot(np.real(min_gs),np.imag(min_gs), marker='o', linestyle='none')
smith.ax.plot(np.real(min_gl),np.imag(min_gl), marker='o', linestyle='none')
plot.grid()



fig2, ay = plot.subplots()
ay.plot(t_line.network.frequencies,t_line.network.phase[1][0])
plot.grid()
plot.show()


