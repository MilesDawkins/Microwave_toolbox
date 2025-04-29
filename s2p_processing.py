import microwave_toolbox as mt
import matplotlib.pyplot as plot
import matplotlib.patches as patches
import numpy as np
import os
import time

##############setup functions####################
start_time = time.time()
script_directory = os.path.dirname(os.path.abspath(__file__))
file = os.path.join(script_directory,"myCPW_005_cpw_with_vias1.s2p")

#################calulation functions###########################
network = mt.system_tools.network(file)

##################plotting functions#######################
#plot.plot(network.frequencies,network.dbmag[1][0])
#plot.plot(network.frequencies,np.real(network.impedance[1][1]))

plot.plot(np.real(network.impedance[0][0]))
plot.plot(np.imag(network.impedance[0][0]))
smith = mt.plotting_tools.smith_chart()
real = [np.real(x) for x in network.complex[0][0]]
imag = [np.imag(x) for x in network.complex[0][0]]
smith.ax.plot(real,imag)

plot.grid()
plot.show()


