import numpy as np
import cmath
import os
import matplotlib.pyplot as plot
from . import system_tools as st


#basic antenna class, contains antenna gain patterns when imported from an antenna test class or known patterns over frequency, also contains an s1p network
#for cascade analysis in the future
class antenna():
    def __init__(self, file_path = None, gain = None, frequencies = None):
            # create class instance globals
            self.sub_type = "antenna"
            self.frequencies = np.array([])
            self.freq_max = 0
            self.freq_min = 0
            self.phi = np.array([])
            self.theta = np.array([])
            self.rad_intensity = np.array([1,1])
            self.p_in = 1
            self.coor_system = "Spherical"
            self.version = ""
            self.freq_unit = ""
            self.format = ""
            self.z_reference = 50


def create_dipole(f0,steps):
    ant = antenna()
    ant.phi = np.linspace(0,2*np.pi,steps)
    ant.theta =  np.linspace(0,np.pi,int(steps/2))
    theta,phi = np.meshgrid(ant.theta,ant.phi)
    l = (3E8/f0)/2
    eta = 120*np.pi
    beta = (2*np.pi)/(3E8/f0)
    ant.rad_intensity.resize([len(ant.phi),len(ant.theta)])
    ant.rad_intensity = 1.64 * (((np.cos(beta*l/2*np.cos(theta)))-np.cos(beta*l/2))/np.sin(theta))**2
    print(len(ant.rad_intensity))
    return ant

def create_isotropic(f0,steps):
    ant = antenna()
    ant.phi = np.linspace(0,2*np.pi,steps)
    ant.theta =  np.linspace(0,np.pi,int(steps/2))
    ant.rad_intensity=np.ones([len(ant.phi),len(ant.theta)])
    print(len(ant.rad_intensity))
    return ant

def create_cos(f0,power,steps, norm_vec = None):
    ant = antenna()
    ant.phi = np.linspace(0,2*np.pi,steps)
    ant.theta =  np.linspace(0,np.pi,int(steps/2))
    theta,phi = np.meshgrid(ant.theta,ant.phi)
    ant.rad_intensity.resize([len(ant.phi),len(ant.theta)])
    ant.rad_intensity = np.cos(theta)**power
    print(len(ant.rad_intensity))
    return ant



#class for defining antenna measurements in a chamber. arguments can be gain over frequency with az/el cuts
class ant_meas():
    def __init__(self, file_path = None, gain = None, frequencies = None):
            
            # create class instance globals
            self.sub_type = "measurement"
            self.frequencies = []
            self.freq_max = 0
            self.freq_min = 0
            self.file_data = [[[]*1]*1]*1
            self.version = ""
            self.freq_unit = ""
            self.format = ""
            self.z_reference = 50


# calculates a boresight gain measurement in an anechoic chamber using the 3 antenna method
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

#calculates the free space path loss based on frequency and distance 
def fspl_calc(freq, distance, dist_units = None):
    if dist_units == "feet":
        factor = 0.305
    elif dist_units == "inches":
        factor = 0.0254
    else:
        factor = 1
    return  10*np.log10(((3E8/freq)/(4*np.pi*(distance*factor)))**2)