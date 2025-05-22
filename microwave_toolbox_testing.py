import microwave_toolbox as mt
import matplotlib.pyplot as plot
import matplotlib.patches as patches
import numpy as np
import os
import time

##############setup functions####################
start_time = time.time()
script_directory = os.path.dirname(os.path.abspath(__file__))
file1 = os.path.join(script_directory,"diy_open2.s1p")
file2 = os.path.join(script_directory,"diy_short_solder2.s1p")

#################calulation functions###########################
open = mt.system_tools.network(file1)
short = mt.system_tools.network(file2)

open_coeff,open_delay = mt.vna_tools.custom_cal_kit_polynomial_calc(open,type = "open")
short_coeff,short_delay = mt.vna_tools.custom_cal_kit_polynomial_calc(short,type = "short")

print(open_coeff,open_delay)
print(short_coeff,short_delay)