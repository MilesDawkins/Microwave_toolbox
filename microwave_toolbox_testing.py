import microwave_toolbox as mt
import matplotlib.pyplot as plot
import numpy as np
import os


file_path = r"C:\Users\Miles\Downloads\Infineon-RFTransistor-SPAR\SPAR\BFP840FESD\BFP840FESD_VCE_2.0V_IC_22mA.s2p"
file_path = file_path.replace("\\", "/")

file_path2 = r"C:\Users\Miles\Downloads\trans_cascade.s2p"
file_path2 = file_path2.replace("\\", "/")


#file_dat = mt.misc.spreadsheet(file_path)
#print(file_dat.col_2_list(4))


trans_s2p = mt.s_param.s_parameter_reader.snp(file_path)
trans_actual = mt.s_param.s_parameter_reader.snp(file_path2)

#print("type :", trans_s2p.linmag[1][0])
figure2, ay = plot.subplots()

test = mt.s_param.s_parameter_cascade.s_param_cascade(trans_s2p,trans_s2p)

testabs = [np.abs(x) for x in test[0][1]]
testdb=[20*np.log10(float(x)) for x in testabs]

plot.plot(trans_s2p.frequencies,testdb)
plot.grid()
plot.plot(trans_actual.frequencies,trans_actual.dbmag[0][1])


#figure3, ap = plot.subplots(np.real(trans_s2p.complex[1][1]))

ax=mt.plot.smith_chart_matplotlib.smith_chart.__init__()
ax.plot(trans_s2p.real[0][0],trans_s2p.imag[0][0])
ax.plot(trans_s2p.real[1][0],trans_s2p.imag[1][0])
ax.plot(trans_s2p.real[0][1],trans_s2p.imag[0][1])
ax.plot(trans_s2p.real[1][1],trans_s2p.imag[1][1])
ax.grid()
ax.set_aspect('equal')

point = 0
for xy in zip(trans_s2p.real[0][0], trans_s2p.imag[0][0]):  
    if point%10 == 0:
        ax.annotate('(%s)' % trans_s2p.frequencies[point], xy=xy, textcoords='data') 
    point = point + 1

plot.show()

