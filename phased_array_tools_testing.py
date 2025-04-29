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
dpp = mt.antenna_tools.create_dipole(2E9)
print("--- %s seconds ---" % (time.time() - start_time))

##################plotting functions#######################
theta90 =int(np.floor(len(dpp.theta)/2))
u =[10*np.log10(dpp.rad_intensity[int(180/4)][x]) for x in range(len(dpp.theta))]
plot.polar(dpp.theta,u)
plot.show()


