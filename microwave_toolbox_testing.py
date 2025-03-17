import microwave_toolbox as mt
import matplotlib.pyplot as plot
import numpy as np
import os


file_path = r"C:\Users\Miles\Downloads\Infineon-RFTransistor-SPAR\SPAR\BFP840FESD\BFP840FESD_VCE_2.0V_IC_22mA.s2p"
file_path = file_path.replace("\\", "/")




#file_dat = mt.misc.spreadsheet(file_path)
#print(file_dat.col_2_list(4))


trans_s2p = mt.network.s_param(file_path)


#print("type :", trans_s2p.linmag[1][0])
figure2, ay = plot.subplots()

test = mt.network.s_param_cascade(trans_s2p,trans_s2p)

testabs = [np.abs(x) for x in test[0][0]]
testreal = [np.real(x) for x in test[0][0]]
testimag = [np.imag(x) for x in test[0][0]]
testdb=[20*np.log10(float(x)) for x in testabs]

plot.plot(trans_s2p.frequencies,testdb)
plot.grid()

ax=mt.plot.smith_chart_matplotlib.smith_chart.__init__()
ax.plot(trans_s2p.real[0][0],trans_s2p.imag[0][0])
ax.plot(testreal,testimag)
ax.grid()
ax.set_aspect('equal')

point = 0
for xy in zip(trans_s2p.real[0][0], trans_s2p.imag[0][0]):  
    if point%10 == 0:
        ax.annotate('(%s)' % trans_s2p.frequencies[point], xy=xy, textcoords='data') 
    point = point + 1

plot.show()

