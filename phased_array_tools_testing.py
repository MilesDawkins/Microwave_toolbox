import microwave_toolbox as mt
import matplotlib.pyplot as plot
import matplotlib.patches as patches
from matplotlib import cm, colors
import numpy as np
import os
import time

##############setup functions####################
start_time = time.time()
script_directory = os.path.dirname(os.path.abspath(__file__))
file = os.path.join(script_directory,"BFP840FESD_VCE_2.0V_IC_22mA.s2p")

#################calulation functions###########################
step_size = 300
num_ele = 16
x_spacing = (3E8/2E9)
delta_phi = np.radians(0)
#weights = [0.357,0.485,0.706,0.890,1,1,0.890,0.706, 0.485,0.357]
dpp = mt.antenna_tools.create_dipole(2E9,step_size)

ele_pos = np.zeros((num_ele,3))
start_x = -(num_ele/4-1)*x_spacing/2
phases = np.zeros(16)
for ele in range (num_ele):
    phases[ele] = ele*delta_phi

for row in range(4):
    for col in range(4):
     print(((row*4)+(col)))
     ele_pos[((row*4)+(col))][2] = start_x+row*x_spacing
     ele_pos[((row*4)+(col))][0] = start_x+col*x_spacing

print(ele_pos)
array = mt.phased_array_tools.element_array(dpp,ele_pos,step_size, phases= phases)
array.calc_array_factor(2E9,step_size)

au = np.zeros((step_size,int(step_size/2)))

for p in range(step_size):
    au[p] = [20*np.log10(x * y) for x,y in zip(array.array_factor[p],dpp.rad_intensity[p])]
    
phi = np.linspace(0,2*np.pi,step_size)
theta = np.linspace(0,np.pi,int(step_size/2))

print("--- %s seconds ---" % (time.time() - start_time))
##################plotting functions#######################
phi_a = np.array(phi)
theta_a = np.array(theta)
threshold = -10
"""
fig, ax = plot.subplots(subplot_kw={'projection': 'polar'})
ax.plot(phi,[au[x][int(step_size/4)] for x in range(len(au))])
ax.set_rlim(-20,40)
plot.show()
"""
mag = np.array(au)
nan_mask = np.isnan(mag)
inf_mask = np.isinf(mag)
less_mask =  mag < threshold
mag[nan_mask|inf_mask|less_mask] = threshold
mag = mag - threshold

theta_grid, phi_grid = np.meshgrid(theta_a, phi_a)
print(mag)

# Convert to Cartesian coordinates
x = mag * np.sin(theta_grid) * np.cos(phi_grid)
y = mag * np.sin(theta_grid) * np.sin(phi_grid)
z = mag * np.cos(theta_grid)
N = np.sqrt(x**2 + y**2 + z**2)
Rmax = np.max(N)
N = N/Rmax

# Create the 3D plot
fig = plot.figure()
ax = fig.add_subplot(111, projection='3d')
mycol = cm.jet(N)
surf = ax.plot_surface(x, y, z, rstride=2, cstride=2, facecolors=mycol, linewidth=0.5, shade=False)  # , alpha=0.5, zorder = 0.5)
#surf = ax.plot_surface(x, y, z,facecolors=mycol)
plot.show()