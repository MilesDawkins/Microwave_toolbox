import microwave_toolbox as mt
import matplotlib.pyplot as plot
import numpy as np
import os


file_path = r"C:\Users\Miles\OneDrive\Documents\Important_stuff\VCU\Senior_Design\actual_ant_s2p.s2p"
ant = mt.network.s_param(file_path)

file_path = r"C:\Users\Miles\OneDrive\Documents\Important_stuff\RF\10GHz EME\Infineon-RFTransistor-SPAR\SPAR\BFP840FESD\BFP840FESD_VCE_2.0V_IC_22mA.s2p"
trans = mt.network.s_param(file_path)

chain = mt.network.s_param_cascade(trans,ant)
print(chain.age)
plot.plot(chain.frequencies,chain.dbmag[1][0])
plot.grid()
plot.xlim([1.5E9,3E9])
plot.xlabel("Frequency (Hz)")
plot.ylabel("S21 (dB)")
plot.title("Single Chain Gain")
plot.show()