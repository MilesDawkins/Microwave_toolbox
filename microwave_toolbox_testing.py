import microwave_toolbox as mt
import matplotlib.pyplot as plot
import numpy as np
import os


file = r"C:\Users\miles\Downloads\BFP840FESD_VCE_2.0V_IC_22mA.s2p"
file = file.replace("\\", "/")
trans_s2p = mt.network.s_param(file_path=file)

print(trans_s2p.dbmag[1][0])

"""
for xy in zip(test.real[0][0], test.imag[0][0]):  
    if point%1000 == 0:
        ax.annotate('(%s)' % (test.frequencies[point]/1E9), xy=xy, textcoords='data') 
    point = point + 1

plot.show()
"""
