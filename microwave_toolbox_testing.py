import microwave_toolbox as mt
import matplotlib.pyplot as plot
import matplotlib.patches as patches
import numpy as np
import os
import time

##############setup functions####################
start_time = time.time()
script_directory = os.path.dirname(os.path.abspath(__file__))
file = os.path.join(script_directory,"example.s2p")

#################calulation functions###########################
freqs = np.linspace(10E9, 10.01E9,1000)
bjt = mt.system_tools.network(file)
dat = np.array(bjt.file_data)

file_data = np.zeros([2,2,4,2],dtype = "object")
print(np.shape(file_data))
print(np.shape(file_data[0][0][0]))
print(np.shape([0,0]))
file_data = np.append(file_data[1,0],[(0,8)],axis = 0)
print(file_data)
print(dat)

