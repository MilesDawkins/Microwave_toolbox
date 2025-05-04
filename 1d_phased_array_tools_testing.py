import microwave_toolbox as mt
import matplotlib.pyplot as plot
from matplotlib import cm, colors
import numpy as np


def find_closest_indices(list_of_numbers, target_value):
    if not list_of_numbers:
        return "The list is empty."
    
    if len(list_of_numbers) == 1:
        return 0, "List has only one element"

    closest_indices = []
    min_diff1 = float('inf')
    min_diff2 = float('inf')
    index1 = -1
    index2 = -1
    
    for index, number in enumerate(list_of_numbers):
        diff = abs(number - target_value)
        
        if diff < min_diff1:
            min_diff2 = min_diff1
            min_diff1 = diff
            index2 = index1
            index1 = index
        elif diff == min_diff1:
             if index != index1:
                min_diff2 = diff
                index2 = index
        elif diff < min_diff2:
            min_diff2 = diff
            index2 = index
            
    if index2 != -1:
        closest_indices = [index1, index2]
    else:
        closest_indices = [index1]
    return closest_indices

#setup functions##############################################################################################################
step_size = 360
f0 = 5E9
num_ele = 10
x_spacing = (3E8/f0)/3
print("Element Spacing (M) = ",x_spacing)
weights = np.ones(num_ele)
#weights = [0.39547,0.506,0.7217,0.8995,1,1,0.8995,0.7217, 0.506,0.39547]

#calculation functions##############################################################################################################

#calcualte dipole pattern
dpp = mt.antenna_tools.create_dipole(f0,step_size)

#setup array based on inputs
ele_pos = np.zeros((num_ele,3))
start_x = -(num_ele/np.sqrt(num_ele)-1)*x_spacing/2
phases = np.zeros(num_ele)
for ele in range(num_ele):
     ele_pos[ele][0] = start_x+ele*x_spacing
     x = ele_pos[ele][0]

#calcualte array factor
array = mt.phased_array_tools.element_array(dpp,ele_pos,step_size,weights = weights)
array.calc_array_factor(f0,step_size)

#calcualte gain based on antenna pattern and array factor
au = np.zeros((step_size,int(step_size/2)))
for p in range(step_size):
    au[p] = [20*np.log10(np.abs(x))+10*np.log10(np.abs(y)) for x,y in zip(array.array_factor[p],dpp.rad_intensity[p])] #-10*np.log10(num_ele)

#calculation HPBW
E_cut = [au[x][int(step_size/4)] for x in range(len(au))]
max_gain = np.nanmax(E_cut)
print("Max Gain (dBi) = ",max_gain)
[hp1,hp2]=find_closest_indices(E_cut,(max_gain-3))

#plotting functions##############################################################################################################

#create array variables for numpy plotting 
phi = np.linspace(0,2*np.pi,step_size)
theta = np.linspace(0,np.pi,int(step_size/2))

#create figure
fig, az = plot.subplots(1,3,subplot_kw={'projection': 'polar'})
fig.suptitle('1D Linear Chebyshev Array, N = '+str(num_ele)+", SLL = -25dB")

#generate E plane Cut
az[0].plot(phi+np.pi/2,[au[x][int(step_size/4)] for x in range(len(au))])
az[0].set_theta_zero_location("E")
az[0].set_rlim(np.nanmax(au)-45,np.nanmax(au)+5)
az[0].set_title("Azimuth Cut")

#create limit line for chebyschev SL level
limit_line = np.full(len(phi),np.nanmax(au)-25)
az[0].plot(phi-np.pi/2,limit_line,color='r',linestyle='--')

#plot HPBW lines
hpa = phi[max([hp1,hp2])]-3*np.pi/2
hpb = phi[min([hp1,hp2])]+3*np.pi/2
hpbw = np.degrees(np.abs(hpa-hpb))
if hpbw >360:
    hpbw = hpbw-360
print("HPBW(deg) = ",(hpbw))
az[0].vlines([-hpa,-hpb],np.nanmax(au)-45 ,np.nanmax(au)+5, zorder=3, colors = ('k','k'), linestyles = 'dashed')

#generate H plane cut
az[1].plot(theta-np.pi/2,[au[int(step_size/4)][x] for x in range(len(au[0]))])
az[1].set_theta_zero_location("E")
az[1].set_rlim(np.nanmax(au)-45,np.nanmax(au)+5)
az[1].set_title("Elevation Cut")

#prepping mag array for 3d plotting
phi_a = np.array(phi)
theta_a = np.array(theta+np.pi)
threshold = np.nanmax(au)-45
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
Rmax = np.nanmax(N)
if Rmax == 0:
    Rmax = 1
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
azs.view_init(elev=30, azim=45)

fig.set_size_inches(15, 5)
plot.show()

