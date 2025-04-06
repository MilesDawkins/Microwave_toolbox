import microwave_toolbox as mt
import matplotlib.pyplot as plot
import matplotlib.patches as patches
import numpy as np
import os
import time

start_time = time.time()

script_directory = os.path.dirname(os.path.abspath(__file__))
file = os.path.join(script_directory,"BFP840FESD_VCE_2.0V_IC_22mA.s2p")
print(mt.antenna_tools.fspl_calc(8E9,8,dist_units = "feet"))
trans_s2p = mt.system_tools.network(file_path=file)
casc=mt.system_tools.network_cascade(trans_s2p,trans_s2p)
#mt.system_tools.reverse_network(trans_s2p)
amp = mt.circuit_tools.rf_amplifier(casc)

smith = mt.plotting_tools.smith_chart()
real = [np.real(x) for x in amp.transistor.complex[1][1]]
imag = [np.imag(x) for x in amp.transistor.complex[1][1]]
smith.ax.plot(real,imag)
plot.grid()
#annotate every 1GHz
point = 0
for xy in zip(real, imag):  
    if amp.frequencies[point]%1E9 == 0:
        smith.ax.annotate('(%s)' % (amp.frequencies[point]/1E9), xy=xy, textcoords='data') 
    point = point + 1

source,load = amp.calc_transducer_impedance(4E9)

sc,sr,lc,lr,min_gs,min_gl = amp.calc_gain_circle(0.5,3E9)
xl = np.real(lc)
yl = np.imag(lc)
xs = np.real(sc)
ys = np.imag(sc)
#smith.ax.add_patch(patches.Circle((xl,yl),lr, edgecolor='r', facecolor='none'))
smith.ax.add_patch(patches.Circle((xs,ys),sr, edgecolor='r', facecolor='none'))
smith.ax.add_patch(patches.Circle((xl,yl),lr, edgecolor='r', facecolor='none'))
print(source*((-1-min_gs)/(min_gs-1)))
print(load*((-1-min_gl)/(min_gl-1)))
smith.ax.plot(np.real(min_gs),np.imag(min_gs), marker='o', linestyle='none')
smith.ax.plot(np.real(min_gl),np.imag(min_gl), marker='o', linestyle='none')


print("--- %s seconds ---" % (time.time() - start_time))
plot.show()


