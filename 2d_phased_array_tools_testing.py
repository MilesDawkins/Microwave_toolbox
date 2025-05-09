import microwave_toolbox as mt
import matplotlib.pyplot as plot
from matplotlib import cm, colors
import numpy as np


#setup functions################################################################################
f0 = 5E9
step_size = 640
num_ele = 10**2
x_spacing = (3E8/f0)/2
print("Element Spacing (M) = ",x_spacing)
steer_theta = 20
steer_phi = 20
weights = np.ones(num_ele)
#calulation functions#############################################################################
dpp = mt.antenna_tools.create_dipole(f0,step_size)

ele_pos = np.zeros((num_ele,3))
start_x = -(num_ele/np.sqrt(num_ele)-1)*x_spacing/2
phases = np.zeros(num_ele)

delta_phi_x = (360*x_spacing*np.sin(np.radians(-steer_phi)))/(3E8/f0)
delta_phi_y = (360*x_spacing*np.sin(np.radians(steer_theta)))/(3E8/f0)
print("Progressive Z Phase Shift(deg) = ",(delta_phi_x))
print("Progressive X Phase Shift(deg) = ",(delta_phi_y))

for row in range(int(np.sqrt(num_ele))):
    for col in range(int(np.sqrt(num_ele))):
     ele_pos[((row*int(np.sqrt(num_ele)))+(col))][2] = start_x+row*x_spacing
     ele_pos[((row*int(np.sqrt(num_ele)))+(col))][0] = start_x+col*x_spacing
     phases[((row*int(np.sqrt(num_ele)))+(col))] = col*np.radians(delta_phi_x) + row*np.radians(delta_phi_y)
print("Element Phases = ", np.rad2deg(phases))

array = mt.phased_array_tools.element_array(dpp,ele_pos,step_size, phases= phases,weights = weights)
array.calc_array_factor(f0,step_size)
au = (20*np.log10(np.abs(array.array_factor))+10*np.log10(np.abs(dpp.rad_intensity))) -10*np.log10(num_ele)
print("Total Array Gain (dBi) = ",np.nanmax(au))

#normalizing gain
au = au-np.nanmax(au)

#plotting functions#################################################################################

#create array variables for numpy plotting 
phi = np.linspace(0,2*np.pi,step_size)
theta = np.linspace(0,np.pi,int(step_size/2))

#create figure
fig, az = plot.subplots(1,3,subplot_kw={'projection': 'polar'})
fig.suptitle(str(int(np.sqrt(num_ele)))+'x'+str(int(np.sqrt(num_ele)))+' Planar Dipole Array Normalized Directivity (dB), Phi = '+str(steer_phi)+', Theta = '+str(steer_theta),fontweight='bold')

az[0].plot(phi+np.pi/2,[au[x][int(step_size/4)] for x in range(len(au))])
az[0].set_theta_zero_location("E")
az[0].set_rlim(np.nanmax(au)-45,np.nanmax(au)+5)
az[0].set_rticks(np.arange(np.nanmax(au)-45,np.nanmax(au)+5,5))  # Less radial ticks
az[0].set_rlabel_position(90)  # Move radial labels away from plotted line
az[0].set_title("Azimuth Cut")

#generate H plane cut
az[1].plot(theta-np.pi/2,[au[int(step_size/4)][x] for x in range(len(au[0]))])
az[1].set_theta_zero_location("E")
az[1].set_rlim(np.nanmax(au)-45,np.nanmax(au)+5)
az[1].set_rticks(np.arange(np.nanmax(au)-45,np.nanmax(au)+5,5))  # Less radial ticks
az[1].set_rlabel_position(90)  # Move radial labels away from plotted line
az[1].set_title("Elevation Cut")

#prepping mag array for 3d plotting
phi_a = np.array(phi)
theta_a = np.array(theta+np.pi)
threshold = np.nanmax(au)-30
mag = np.array(au)
nan_mask = np.isnan(mag)
inf_mask = np.isinf(mag)
less_mask =  mag < threshold
mag[nan_mask|inf_mask|less_mask] = threshold
mag = mag - threshold
mag = mag-np.min(mag)
theta_grid, phi_grid = np.meshgrid(theta_a, phi_a)

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
azs.set_title("3D Radiation Pattern")
azs.view_init(elev=30, azim=60)

fig.set_size_inches(15, 5.5)
plot.show()

