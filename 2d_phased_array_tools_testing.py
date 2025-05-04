import microwave_toolbox as mt
import matplotlib.pyplot as plot
from matplotlib import cm, colors
import numpy as np


#setup functions################################################################################

step_size = 360
num_ele = 5**2
x_spacing = (3E8/2E9)/2
steer_theta = -00
steer_phi = -00

#calulation functions#############################################################################
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
    

#plotting functions#################################################################################
#create array variables for numpy plotting 
phi = np.linspace(0,2*np.pi,step_size)
theta = np.linspace(0,np.pi,int(step_size/2))

#generate E plane cut
fig, az = plot.subplots(1,3,subplot_kw={'projection': 'polar'})
az[0].plot(phi-np.pi/2,[au[x][int(step_size/4)] for x in range(len(au))])
az[0].set_theta_zero_location("S")
lines, labels = plot.thetagrids(range(0, 360, 10),range(180, -180, -10))
az[0].set_rlim(np.nanmax(au)-30,np.nanmax(au)+5)


#generate H plane cut
az[1].plot(theta+np.pi/2,[au[int(step_size/4)][x] for x in range(len(au[0]))])
az[1].set_theta_zero_location("W")
lines, labels = plot.thetagrids(range(0, 360, 10),range(-180, 180, 10))
az[1].set_rlim(np.nanmax(au)-30,np.nanmax(au)+5)

#prepping mag array for 3d plotting
phi_a = np.array(phi)
theta_a = np.array(theta)
threshold = np.nanmax(au)-30
mag = np.array(au)
nan_mask = np.isnan(mag)
inf_mask = np.isinf(mag)
less_mask =  mag < threshold
mag[nan_mask|inf_mask|less_mask] = threshold
mag = mag - threshold
mag = mag-np.min(mag)
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
az[2].remove()
azs = fig.add_subplot(1,3,3, projection='3d')
mycol = cm.jet(N)
surf = azs.plot_surface(x, y, z, rstride=3, cstride=3, facecolors=mycol, linewidth=0.5, shade=False)
limits = np.r_[azs.get_xlim3d(), azs.get_ylim3d(), azs.get_zlim3d()]
limits = [np.min(limits, axis=0), np.max(limits, axis=0)]
azs.set(xlim3d=limits, ylim3d=limits, zlim3d=limits, box_aspect=(1, 1, 1))
plot.show()