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
freqs = np.linspace(1E9, 10E9,1000)
bjt = mt.system_tools.network(file)

f0 = 6E9
sl = 0.25
pl = 0.25

z1 = 50
z2 = 30.1
z12 = 48.4
z23 = 49.1


shunt_match1 = mt.t_line_tools.microstrip(z1,4.4,1.6E-3,sl,freqs_in = freqs, typem="short", shunt_in=True, length_unit="lambda", center_freq = f0)
shunt_match2 = mt.t_line_tools.microstrip(z2,4.4,1.6E-3,sl,freqs_in = freqs, typem="short", shunt_in=True, length_unit="lambda", center_freq = f0)

phase_match1 = mt.t_line_tools.microstrip(z12,4.4,1.6E-3,pl,freqs_in = freqs, length_unit="lambda", center_freq= f0)
phase_match2 = mt.t_line_tools.microstrip(z12,4.4,1.6E-3,pl,freqs_in = freqs, length_unit="lambda", center_freq= f0)

tl = mt.t_line_tools.microstrip(50,4.4,1.6E-3,0.01,freqs_in = freqs,zl_in=25)

network = shunt_match1.network ** phase_match1.network ** shunt_match2.network ** phase_match2.network ** shunt_match2.network ** phase_match1.network ** shunt_match1.network ** tl.network

print("--- %s seconds ---" % (time.time() - start_time))

##################plotting functions#######################
#plot.plot(network.frequencies,network.dbmag[1,0])
plot.plot(network.frequencies,network.dbmag)

plot.grid()
plot.show()


