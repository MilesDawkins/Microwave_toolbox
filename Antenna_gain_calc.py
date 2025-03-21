import microwave_toolbox as mt
import matplotlib.pyplot as plot
import numpy as np
import os


file_path = r"C:\Users\Miles\OneDrive\Documents\Important_stuff\VCU\Senior_Design\vcus21_7ft_hor.s2p"
file_path = file_path.replace("\\", "/")
channel_1 = mt.network.s_param(file_path)
channel_1.dbmag[1][0] = [x for x in channel_1.dbmag[1][0]]
plot.plot(channel_1.frequencies,channel_1.dbmag[1][0])
plot.grid()
plot.xlim([1.5E9,3E9])
plot.ylim([-60,0])
plot.xlabel("Frequency (Hz)")
plot.ylabel("dBmag S21")
plot.title("Array H-pol 7 Feet Distance")
plot.show()


#plot actual pattern
file_path = r"C:\Users\Miles\Downloads\lindgren_3102_gain.csv"
file_path = file_path.replace("\\", "/")
file_dat = mt.misc.spreadsheet(file_path, titled = True)

freq = file_dat.col_2_list(0)
gain = file_dat.col_2_list(1)


freqf = [float(item)*1E9 for item in freq]
gainf = [float(item) for item in gain]

plot.figure()
plot.plot(freqf,gainf)
plot.show()

gain_interp = []
fspl = []
gain_calc = []
single_el = []
for f in range(len(channel_1.frequencies)):
        #interpolate value at frequency point
        gain_interp.append(np.interp(channel_1.frequencies[f],freqf,gainf))
        fspl.append(10*np.log10(((3E8/channel_1.frequencies[f])/(np.pi*4*2.5))**2))
        gain_calc.append(channel_1.dbmag[1][0][f]-fspl[f]+gain_interp[f]-3+30)
        single_el.append(gain_calc[f]-10)

plot.figure()
plot.plot(channel_1.frequencies,gain_calc)
plot.plot(channel_1.frequencies,single_el)
plot.xlabel("Frequency (Hz)")
plot.ylabel("Full System Gain (dB)")
plot.title("Array H-pol 7 Foot Distance")
plot.xlim([1.5E9,3E9])
plot.ylim([0,70])
plot.grid()
plot.show()