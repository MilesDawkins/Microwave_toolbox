import microwave_toolbox as mt
import matplotlib.pyplot as plot
import numpy as np
"""
a=mt.t_line.microstrip(50,4.4,1.6E-3)
print(a.width)
a.length = 1
print(a.input_z(3E9,0.05,50))
print(a.input_z(1E9,0.01,0))

file_path = 'C:/Users/miles/Downloads/Infineon-RFTransistor-SPAR/SPAR/BFP840FESD/BFP840FESD_VCE_2.0V_IC_22mA.s2p'  # Replace with your S2P file path
#file_path = 'C:/Users/miles/OneDrive/Documents/Important_stuff/RF/10GHz EME/Python_scripts/example.s3p'
trans_s2p = mt.s_param.s_parameter_reader.snp(file_path)


#print("type :", trans_s2p.linmag[1][0])
ax=mt.plot.smith_chart_matplotlib.smith_chart.__init__()
ax.plot(trans_s2p.real[0][0],trans_s2p.imag[0][0])
#plot.plot(trans_s2p.real[1][0],trans_s2p.imag[1][0])
ax.plot(trans_s2p.real[0][1],trans_s2p.imag[0][1])
ax.plot(trans_s2p.real[1][1],trans_s2p.imag[1][1])
ax.grid()
ax.set_aspect('equal')

plot.show()

"""
x = np.linspace(0, 5,100)
a = np.cos(((2*np.pi)/0.6)*x*np.cos(np.pi/4))
plot.plot(x,a)
plot.show()