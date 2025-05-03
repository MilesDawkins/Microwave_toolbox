import microwave_toolbox as mt
import matplotlib.pyplot as plot
import matplotlib.patches as patches
from matplotlib import cm, colors
import numpy as np
import os
import time

##############setup functions####################
start_time = time.time()
step_size = 300
num_ele = 6**2
x_spacing = (3E8/2E9)/2
steer_theta = -0
steer_phi = -30

#weights = [0.357,0.485,0.706,0.890,1,1,0.890,0.706, 0.485,0.357]

#################calulation functions###########################
dpp = mt.antenna_tools.create_dipole(2E9,step_size)

ele_pos = np.zeros((num_ele,3))
start_x = -(num_ele/np.sqrt(num_ele)-1)*x_spacing/2
phases = np.zeros(num_ele)

delta_phi_x = np.radians((360*x_spacing*np.sin(np.radians(steer_theta)))/(3E8/2E9))
delta_phi_y = np.radians((360*x_spacing*np.sin(np.radians(steer_phi)))/(3E8/2E9))

for row in range(int(np.sqrt(num_ele))):
    for col in range(int(np.sqrt(num_ele))):
     print(((row*int(np.sqrt(num_ele)))+(col)))
     ele_pos[((row*int(np.sqrt(num_ele)))+(col))][2] = start_x+row*x_spacing
     ele_pos[((row*int(np.sqrt(num_ele)))+(col))][0] = start_x+col*x_spacing
     phases[((row*int(np.sqrt(num_ele)))+(col))] = col*delta_phi_x + row*delta_phi_y

print(ele_pos)
array = mt.phased_array_tools.element_array(dpp,ele_pos,step_size, phases= phases)
array.calc_array_factor(2E9,step_size)

au = np.zeros((step_size,int(step_size/2)))

for p in range(step_size):
    au[p] = [10*np.log10(np.abs(x * y)) for x,y in zip(array.array_factor[p],dpp.rad_intensity[p])]
    
phi = np.linspace(0,2*np.pi,step_size)
theta = np.linspace(0,np.pi,int(step_size/2))

print("--- %s seconds ---" % (time.time() - start_time))
##################plotting functions#######################
phi_a = np.array(phi)
theta_a = np.array(theta)
threshold = -10

fig, ay = plot.subplots(subplot_kw={'projection': 'polar'})
ay.plot(phi-np.pi/2,[au[x][int(step_size/4)] for x in range(len(au))])
ay.set_theta_zero_location("S")
lines, labels = plot.thetagrids(range(0, 360, 10),range(180, -180, -10))
ay.set_rlim(-20,20)
plot.show()

fig, az = plot.subplots(subplot_kw={'projection': 'polar'})
az.plot(theta+np.pi/2,[au[int(step_size/4)][x] for x in range(len(au[0]))])
az.set_theta_zero_location("W")
lines, labels = plot.thetagrids(range(0, 360, 10),range(-180, 180, 10))
az.set_rlim(-20,20)
plot.show()

#prepping mag array for 3d plotting
mag = np.array(au)
nan_mask = np.isnan(mag)
inf_mask = np.isinf(mag)
less_mask =  mag < threshold
mag[nan_mask|inf_mask|less_mask] = threshold
mag = mag - threshold
mag = mag-np.min(mag)
theta_grid, phi_grid = np.meshgrid(theta_a, phi_a)
print(mag)

"""
mag = np.array(au)
nan_mask = np.isnan(mag)
inf_mask = np.isinf(mag)
mag[nan_mask|inf_mask] = np.min(mag[np.isfinite(mag)])
mag = mag+np.abs(np.min(mag))
mag = mag/np.max(mag)
theta_grid, phi_grid = np.meshgrid(theta_a, phi_a)
print(mag)
"""

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
surf = ax.plot_surface(x, y, z, rstride=3, cstride=3, facecolors=mycol, linewidth=0.5, shade=False)  # , alpha=0.5, zorder = 0.5)
limits = np.r_[ax.get_xlim3d(), ax.get_ylim3d(), ax.get_zlim3d()]
limits = [np.min(limits, axis=0), np.max(limits, axis=0)]
ax.set(xlim3d=limits, ylim3d=limits, zlim3d=limits, box_aspect=(1, 1, 1))
#surf = ax.plot_surface(x, y, z,facecolors=mycol)
plot.show()