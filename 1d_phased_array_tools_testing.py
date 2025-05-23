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
step_size = 600
f0 = 1E9
num_ele = 1
plot_thresh = -40
x_spacing = 0.035#(3E8/f0)/4
print("Element Spacing (M) = ",x_spacing)
weights = np.ones(num_ele)
phases = np.zeros(num_ele)
#weights = [0.39547,0.506,0.7217,0.8995,1,1,0.8995,0.7217, 0.506,0.39547]
#weights = [-1,-1,-1,-1,-1,1,1,1,1,1]

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
     #phases[ele] = np.pi/2*ele

#calcualte array factor
array = mt.phased_array_tools.element_array(dpp,ele_pos,step_size,weights = weights,phases = phases)
array.calc_array_factor(f0,step_size)

#calcualte gain based on antenna pattern and array factor
au = (20*np.log10(np.abs(array.array_factor))+10*np.log10(np.abs(dpp.rad_intensity))) -10*np.log10(num_ele)
print("Total Array Gain (dBi) = ",np.nanmax(au))

#normalizing gain
au = au-np.nanmax(au)
au_lin = 10**(au/10)
#calculation HPBW
E_cut = [au[x][int(step_size/4)] for x in range(len(au))]
max_gain = np.nanmax(E_cut)

#numerical directiviy integration and calcualtion
inte = 0
inte1 = 0
phi = np.linspace(0,2*np.pi,step_size)
theta = np.linspace(0,np.pi,int(step_size/2))
for p in range(len(phi)):
    inte1 = 0
    for t in range(len(theta)):
        inte1 = inte1 + (np.pi/step_size/2) * au_lin[p,t] * np.sin(theta[t])
    inte = inte + inte1 * ((2*np.pi)/step_size)
do=10*np.log10(np.nanmax(au_lin)/(1/(4*np.pi)*(inte))) - 6.03514053150483# #not sure where the 6 is coming from but this gets me the same values as balanis, for cos elements divide 6 factor by 2 (why?), fordipole subtract 1.355 on top of 6 factor (only ofr arrays?)
print(do)
#[hp1,hp2]=find_closest_indices(E_cut,(max_gain-3))

#plotting functions##############################################################################################################

#create array variables for numpy plotting 
phi = np.linspace(0,2*np.pi,step_size)
theta = np.linspace(0,np.pi,int(step_size/2))

#create figure
fig, az = plot.subplots(1,3,subplot_kw={'projection': 'polar'})
fig.suptitle('1D Linear Chebyshev Array Normalized Directivity (dB), N = '+str(num_ele)+", SLL = -25dB",fontweight='bold')
#fig.suptitle('1D Linear Array Normalized Directivity (dB), N = '+str(num_ele),fontweight='bold')
#fig.suptitle('Single Dipole Element Normalized Radiation Pattern (dB)',fontweight='bold')

#generate E plane Cut
az[0].plot(phi+np.pi/2,[au[x][int(step_size/4)] for x in range(len(au))])
az[0].set_theta_zero_location("E")
az[0].set_rlim(np.nanmax(au)+plot_thresh,np.nanmax(au)+5)
az[0].set_rticks(np.arange(np.nanmax(au)+plot_thresh,np.nanmax(au)+5,5))  # Less radial ticks
az[0].set_rlabel_position(90)  # Move radial labels away from plotted line
az[0].set_title("Azimuth Cut")

if(0):
    #create limit line for chebyschev SL level
    limit_line = np.full(len(phi),np.nanmax(au)-25)
    az[0].plot(phi,limit_line,color='r',linestyle='--')

    #plot HPBW lines
    hpa = phi[max([hp1,hp2])]-3*np.pi/2
    hpb = phi[min([hp1,hp2])]+3*np.pi/2
    hpbw = np.degrees(np.abs(hpa-hpb))
    if hpbw >360:
        hpbw = hpbw-360
    print("HPBW(deg) = ",(hpbw))
    az[0].vlines([-hpa,-hpb],np.nanmax(au)+plot_thresh ,np.nanmax(au)+5, zorder=3, colors = ('k','k'), linestyles = 'dashed')

#generate H plane cut
az[1].plot(theta,[au[int(step_size/2)][x] for x in range(len(au[0]))])
az[1].set_theta_zero_location("E")
az[1].set_rlim(np.nanmax(au)+plot_thresh,np.nanmax(au)+5)
az[1].set_rticks(np.arange(np.nanmax(au)+plot_thresh,np.nanmax(au)+5,5))  # Less radial ticks
az[1].set_rlabel_position(90)  # Move radial labels away from plotted line
az[1].set_title("Elevation Cut")

#prepping mag array for 3d plotting
phi_a = np.array(phi)
theta_a = np.array(theta)
threshold = np.nanmax(au)+plot_thresh
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

fig.set_size_inches(15, 5.5)
plot.show()

