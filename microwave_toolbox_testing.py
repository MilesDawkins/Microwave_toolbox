import microwave_toolbox as mt
import matplotlib.pyplot as plot
import matplotlib.patches as patches
import numpy as np
import os
import time

##############setup functions####################
start_time = time.time()
script_directory = os.path.dirname(os.path.abspath(__file__))
file1 = os.path.join(script_directory,"diy_open2_filtered_12GHz.s1p")
file2 = os.path.join(script_directory,"diy_short_solder2.s1p")
file3 = os.path.join(script_directory,"diy_load2.s1p")

#################calulation functions###########################
open = mt.system_tools.network(file1)
short = mt.system_tools.network(file2)
load = mt.system_tools.network(file3)

open_coeff,open_delay = mt.vna_tools.custom_cal_kit_polynomial_calc(open,type = "open")
short_coeff,short_delay = mt.vna_tools.custom_cal_kit_polynomial_calc(short,type = "short")
load_coeff,load_delay = mt.vna_tools.custom_cal_kit_polynomial_calc(load,type = "load")

print(open_coeff,open_delay)
print(short_coeff,short_delay)
print(load_coeff,load_delay)