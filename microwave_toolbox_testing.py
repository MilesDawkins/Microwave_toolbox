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
freqs = np.linspace(1E6,10E9,1000)
stub_load = [1/(1j*2*np.pi*x*10E-12) for x in freqs]

t_line = mt.t_line_tools.microstrip(50,4.4,1.6E-3, typem = "open")
t_line_2 = mt.t_line_tools.microstrip(50,4.4,1.6E-3, typem = "loaded", zl_in = 115)
t_line.create_network(freqs,21.3E-3)
t_line_2.create_network(freqs,8.649E-3)
z=[]
print(t_line.ereff)
for f in range(len(freqs)):
    z.append(1/(1/t_line.network.impedance[f]+1/t_line_2.network.impedance[f]))
#t_cascade = mt.system_tools.network_cascade(t_line_2.network,t_line.network)
plot.plot(t_line.network.frequencies,[20*np.log10(np.abs((x-50)/(x+50))) for x in z])
print("--- %s seconds ---" % (time.time() - start_time))

90


##################plotting functions#######################
smith = mt.plotting_tools.smith_chart()
real = [np.real(x) for x in z]
imag = [np.imag(x) for x in z]
smith.ax.plot(real,imag)
#smith.ax.plot(real,imag)

"""
    #annotate every 1GHz
point = 0
for xy in zip(real, imag):  
    if amp.frequencies[point]%1E9 == 0:
        smith.ax.annotate('(%s)' % (amp.frequencies[point]/1E9), xy=xy, textcoords='data') 
        smith.ax.plot(real2[point],imag2[point], marker='o',markersize = 2 , c='black', linestyle='none')
    point = point + 1
"""

plot.grid()



#fig2, ay = plot.subplots()
plot.grid()
plot.show()


