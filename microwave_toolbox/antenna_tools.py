import numpy as np
import cmath
import os
import matplotlib.pyplot as plot
from . import system_tools as st



def range_gain_calculator(ref_gain: st.network, ref_thru: st.network, aut_thru: st.network, delta_len = None, interp_freq_ste = None):
    if len(ref_thru) != len(aut_thru):
        print("CAUTION: Number of range calibration points not equal")

    if  interp_freq_step == None:
        interp_freq_step = 10E6
    #determine frequencies that cascade can be performed
    f_min = min(ref_gain)
    f_max = min(s1.frequencies[(len(s1.frequencies)-1)],s2.frequencies[(len(s2.frequencies)-1)])
    freq=np.arange(start=f_min,stop=f_max+interp_freq_step,step=interp_freq_step)
    
    #range loss calc = ref thru - ref gain

    #aut gain calc = aut_thru + range loss

    return

def fspl_calc(freq, distance, dist_units = None):
    if dist_units == "feet":
        factor = 0.305
    elif dist_units == "inches":
        factor = 0.0254
    else:
        factor = 1
    return  10*np.log10(((3E8/freq)/(4*np.pi*(distance*factor)))**2)