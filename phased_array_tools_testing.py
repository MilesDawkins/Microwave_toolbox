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


num_ele = 10
x_spacing = (3E8/2E9)/2

ele_pos = np.zeros((num_ele,3))
start_x = -(num_ele-1)*x_spacing/2
weights = [0.357,0.485,0.706,0.890,1,1,0.890,0.706, 0.485,0.357]
for x in range(num_ele):
    ele_pos[x][2] = start_x+x*x_spacing
array = mt.phased_array_tools.element_array(dpp,ele_pos, weights = weights)
array.calc_array_factor(2E9)

af = [array.array_factor[90][x] for x in range(len(array.array_factor[180]))]
du = [dpp.rad_intensity[int(180/4)][x] for x in range(int(np.floor(len(dpp.phi))))]

au = [20*np.log10(np.abs(x)*np.abs(y)) for x,y in zip(af,du)]
theta = np.linspace(0,np.pi,181)

fig, ax = plot.subplots(subplot_kw={'projection': 'polar'})
ax.plot(theta,au)
ax.set_rlim(-20,40)
plot.show()


