import microwave_toolbox as mt
import matplotlib.pyplot as plot
import numpy as np
import os, sys
import time


start_time = time.time()

script_directory = os.path.dirname(os.path.abspath(__file__))
file = os.path.join(script_directory,"BFP840FESD_VCE_2.0V_IC_22mA.s2p")
print(mt.antenna_tools.fspl_calc(1E9,8,dist_units = "feet"))
trans_s2p = mt.system_tools.network(file_path=file)
#mt.system_tools.reverse_network(trans_s2p)
cascade = mt.system_tools.network_cascade(trans_s2p,trans_s2p,10E6)

plot.plot(cascade.frequencies,cascade.dbmag[1][0])
ax=mt.plot.smith_chart_matplotlib.smith_chart.__init__()
ax.plot([np.real(x) for x in cascade.complex[1][1]],[np.imag(y) for y in cascade.complex[1][1]])
ax.grid()
ax.set_aspect('equal')
plot.show()


print("--- %s seconds ---" % (time.time() - start_time))