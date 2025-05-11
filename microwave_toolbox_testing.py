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
freqs = np.linspace(10E9, 10.01E9,1000)
bjt = mt.system_tools.network(file)
bjt2 = bjt** bjt
plot.plot(bjt2.frequencies,bjt2.dbmag[0,0])
plot.show()