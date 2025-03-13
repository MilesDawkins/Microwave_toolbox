import microwave_toolbox as mt
import matplotlib.pyplot as plot
import numpy as np
import os

a=mt.t_line.microstrip(50,4.4,1.6E-3)
print(a.width)
a.length = 1
print(a.input_z(3E9,0.05,50))
print(a.input_z(1E9,0.01,0))

file_path = r"C:\Users\Miles\Downloads\Infineon-RFTransistor-SPAR\SPAR\BFP840FESD\BFP840FESD_VCE_2.0V_IC_22mA.s2p"
file_path = file_path.replace("\\", "/")
trans_s2p = mt.s_param.s_parameter_reader.snp(file_path)


#print("type :", trans_s2p.linmag[1][0])
figure2, ay = plot.subplots()
ay.plot(trans_s2p.frequencies,trans_s2p.dbmag[1][1])

ax=mt.plot.smith_chart_matplotlib.smith_chart.__init__()
ax.plot(trans_s2p.real[0][0],trans_s2p.imag[0][0])
ax.plot(trans_s2p.real[1][0],trans_s2p.imag[1][0])
ax.plot(trans_s2p.real[0][1],trans_s2p.imag[0][1])
ax.plot(trans_s2p.real[1][1],trans_s2p.imag[1][1])
ax.grid()
ax.set_aspect('equal')

point = 0
for xy in zip(trans_s2p.real[1][0], trans_s2p.imag[1][0]):  
    if point%10 == 0:
        ax.annotate('(%s)' % trans_s2p.frequencies[point], xy=xy, textcoords='data') 
    point = point + 1

plot.show()

