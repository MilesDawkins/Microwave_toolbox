import microwave_toolbox as mt
import matplotlib.pyplot as plot
import matplotlib.patches as patches
import numpy as np
import os
import time

##############setup functions####################
start_time = time.time()
script_directory = os.path.dirname(os.path.abspath(__file__))
file1 = os.path.join(script_directory,"BFP840FESD_VCE_2.0V_IC_22mA.s2p")
file2 = os.path.join(script_directory,"BFCN-1560+___Plus25degC.s2p")

#################calulation functions###########################
