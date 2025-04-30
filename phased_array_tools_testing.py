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
step_size = 361
num_ele = 10
x_spacing = (3E8/2E9)/2
delta_phi = np.radians(0)
weights = [0.357,0.485,0.706,0.890,1,1,0.890,0.706, 0.485,0.357]
dpp = mt.antenna_tools.create_dipole(2E9,step_size)

ele_pos = np.zeros((num_ele,3))
start_x = -(num_ele-1)*x_spacing/2
phases = np.zeros(10)
for ele in range (num_ele):
    phases[ele] = ele*delta_phi

for x in range(num_ele):
    ele_pos[x][2] = start_x+x*x_spacing
array = mt.phased_array_tools.element_array(dpp,ele_pos,step_size,weights = weights, phases= phases)
array.calc_array_factor(2E9,step_size)

au = np.zeros((step_size,int(step_size/2)))

for p in range(step_size):
    au[p] = [(x * y) for x,y in zip(array.array_factor[p],dpp.rad_intensity[p])]
    
phi = np.linspace(0,2*np.pi,step_size)
theta = np.linspace(0,np.pi,int(step_size/2))

print("--- %s seconds ---" % (time.time() - start_time))
##################plotting functions#######################
"""
data_array = np.array(au)
x_dim, y_dim = data_array.shape
x_axis, y_axis = np.meshgrid(np.arange(x_dim), np.arange(y_dim))

fig = plot.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(x_axis, y_axis, data_array.T)

plot.show()

"""
"""
fig, ax = plot.subplots(subplot_kw={'projection': 'polar'})
ax.plot(phi,[au[x][int(step_size/4)] for x in range(len(au))])
ax.set_rlim(-20,40)
plot.show()
"""
mag = np.array(au)
nan_mask = np.isnan(mag)
inf_mask = np.isinf(mag)
mag[nan_mask|inf_mask] = -30

phi_a = np.array(phi)
theta_a = np.array(theta)

theta_grid, phi_grid = np.meshgrid(theta_a, phi_a)
print(mag)
# Convert to Cartesian coordinates
x = mag * np.sin(theta_grid) * np.cos(phi_grid)
y = mag * np.sin(theta_grid) * np.sin(phi_grid)
z = mag * np.cos(theta_grid)

# Create the 3D plot
fig = plot.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(x, y, z, cmap='jet')
plot.show()