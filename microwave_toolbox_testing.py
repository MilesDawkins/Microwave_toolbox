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
freqs = np.linspace(1E9,10E9,1000)
stub_load = [1/(1j*2*np.pi*x*10E-12) for x in freqs]

print(mt.antenna_tools.fspl_calc(2.1E9,102,dist_units="inches"))

t_line = mt.t_line_tools.microstrip(50,4.4,1.6E-3,21.3E-3,freqs_in = freqs, typem = "open")
t_line_s = mt.t_line_tools.microstrip(25,1,1.6E-3,37.5E-3,freqs_in=freqs, typem = "short", shunt_in=True)
t_line_2 = mt.t_line_tools.microstrip(70.7,4.4,1.6E-3,10E-3, freqs_in=freqs, typem = "loaded", zl_in = 100)
t_line_3 = mt.t_line_tools.microstrip(100,1,1.6E-3,20E-3,freqs_in = freqs)


shunt_t_line_cascade = mt.system_tools.network_cascade(t_line_3.network,t_line_s.network)
shunt_t_line_cascade = mt.system_tools.network_cascade(shunt_t_line_cascade,t_line_3.network)

z=[]
for f in range(len(freqs)):
    z.append(1/(1/t_line.network.impedance[f]+1/t_line_2.network.impedance[f]))
z_gamma = [(x-50)/(x+50) for x in z]


#t_cascade = mt.system_tools.network_cascade(t_line_2.network,t_line.network)
#plot.plot(t_line.network.frequencies,[20*np.log10(abs(x)) for x in z_gamma])
plot.plot(shunt_t_line_cascade.frequencies,shunt_t_line_cascade.dbmag[1][0])
print("--- %s seconds ---" % (time.time() - start_time))
plot.ylim([-40,10])

##################plotting functions#######################
smith = mt.plotting_tools.smith_chart()
real = [np.real(x) for x in z_gamma]
imag = [np.imag(x) for x in z_gamma]
smith.ax.plot(real,imag)
#smith.ax.plot(real,imag)


    #annotate every 1GHz
point = 0
for xy in zip(real, imag):  
    if t_line.network.frequencies[point]%1E9 == 0:
        smith.ax.annotate('(%s)' % (t_line.network.frequencies[point]/1E9), xy=xy, textcoords='data') 
        smith.ax.plot(real[point],imag[point], marker='o',markersize = 2 , c='black', linestyle='none')
    point = point + 1


plot.grid()



#fig2, ay = plot.subplots()
plot.grid()
plot.show()


