import microwave_toolbox as mt
import matplotlib.pyplot as plot
import numpy as np
import os


file_path = r"C:\Users\Miles\OneDrive\Documents\Important_stuff\VCU\Senior_Design\actual_ant_s2p.s2p"
file_path = file_path.replace("\\", "/")
channel_1 = mt.network.s_param(file_path)
plot.plot(channel_1.frequencies,channel_1.phase[1][1])
plot.grid()
plot.xlim([1.5E9,3E9])
plot.xlabel("Frequency (Hz)")
plot.ylabel("S21 (dB)")
plot.title("Single Chain Gain")
plot.show()