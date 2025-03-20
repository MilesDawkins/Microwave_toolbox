import microwave_toolbox as mt
import matplotlib.pyplot as plot
import numpy as np
import os


file_path = r"C:\Users\Miles\OneDrive\Documents\Important_stuff\VCU\Senior_Design\vcus21_7ft_hor.s2p"
file_path = file_path.replace("\\", "/")
channel_1 = mt.s_param.s_parameter_reader.snp(file_path)
channel_1.dbmag[1][0] = [x for x in channel_1.dbmag[1][0]]
plot.plot(channel_1.frequencies,channel_1.dbmag[1][0])
plot.grid()
plot.xlim([1.5E9,3E9])
plot.ylim([-60,0])
plot.xlabel("Frequency (Hz)")
plot.ylabel("dBmag S21")
plot.title("Array H-pol 7 Feet Distance")
plot.show()
