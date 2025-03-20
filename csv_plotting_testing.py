import microwave_toolbox as mt
import matplotlib.pyplot as plot
import numpy as np
import os

#plot actual pattern
file_path = r"C:\Users\Miles\OneDrive\Documents\Important_stuff\VCU\Senior_design_antenna_recovered\actual_boresight_gain.csv"
file_path = file_path.replace("\\", "/")
file_dat = mt.misc.spreadsheet(file_path, titled = True)

theta = file_dat.col_2_list(2)
mag = file_dat.col_2_list(3)
phi = file_dat.col_2_list(1)

phif = [float(item) for item in phi]
thetaf = [float(item) for item in theta]
magf = [float(item) for item in mag]
i=0

theta_az = []
theta_el = []
mag_az = []
mag_el = []

while phi[i] != '90':
    theta_az.append(thetaf[i])
    mag_az.append(magf[i])
    i = i+1

while phi[i] == '90':
    print(phi[i])
    theta_el.append(thetaf[i])
    mag_el.append(magf[i])
    i = i+1
    if i >= len(magf):
        break

plot.figure()
plot.plot(theta_az,mag_az)
plot.plot(theta_el,mag_el)




# Plot simmed pattern
file_path = r"C:\Users\Miles\OneDrive\Documents\Important_stuff\VCU\Senior_design_antenna_recovered\array_gain_plot_no_steer.csv"
file_path = file_path.replace("\\", "/")
file_dat = mt.misc.spreadsheet(file_path, titled = True)


theta = file_dat.col_2_list(2)
mag = file_dat.col_2_list(3)
phi = file_dat.col_2_list(1)

phif = [float(item) for item in phi]
thetaf = [float(item) for item in theta]
magf = [float(item) for item in mag]
i=0

theta_az = []
theta_el = []
mag_az = []
mag_el = []

while phi[i] != '90':
    theta_az.append(thetaf[i]-90)
    mag_az.append(magf[i])
    i = i+1

while phi[i] == '90':
    theta_el.append(thetaf[i])
    mag_el.append(magf[i])
    i = i+1
    if i >= len(magf):
        break

plot.figure()
plot.plot(theta_az,mag_az)
plot.plot(theta_el,mag_el)
plot.show()