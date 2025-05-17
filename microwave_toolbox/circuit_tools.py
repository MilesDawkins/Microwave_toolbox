import numpy as np
import cmath
import os
from . import system_tools as st
from . import plotting_tools


class rf_amplifier():
    """
    references for this tool:
    https://www.allaboutcircuits.com/technical-articles/designing-a-unilateral-rf-amplifier-for-a-specified-gain/
    https://www.allaboutcircuits.com/technical-articles/learn-about-unconditional-stability-and-potential-instability-in-rf-amplifier-design/
    https://www.allaboutcircuits.com/technical-articles/learn-about-designing-unilateral-low-noise-amplifiers/
    https://www.allaboutcircuits.com/technical-articles/bilateral-rf-amplifier-design-simultaneous-conjugate-matching-for-maximum-gain/
    https://www.allaboutcircuits.com/technical-articles/using-the-operating-power-gain-to-design-a-bilateral-rf-amplifier/
    "Microwave Transistor Amplifiers 2nd Edition" by Guillermo Gonzalez
    """
    def __init__(self, s2p_in: st.network):
        #initialize basic variables
        self.type = "Amplifier"
        self.sub_type = "None"
        self.z_reference = 50
        self.transistor = s2p_in
        self.frequencies = s2p_in.frequencies

        self.source_max_gain = 1/(1-abs(self.transistor.complex[0,0])**2)
        self.source_max_gain_gamma = np.conjugate(self.transistor.complex[0,0])

        self.load_max_gain = 1/(1-abs(self.transistor.complex[1,1])**2)
        self.load_max_gain_gamma = np.conjugate(self.transistor.complex[1,1])

        self.max_z0_transducer_gain = abs(self.transistor.complex[1,0])**2

        self.max_transducer_gain = self.load_max_gain*self.source_max_gain*self.max_z0_transducer_gain
    
    def calc_gain_circle(self,source_or_load: str,log_gain,freq):
        gain = 10**(log_gain/10)
        g_s_max = np.interp(freq,self.frequencies,self.source_max_gain)
        g_s_norm = gain/g_s_max
        g_l_max = np.interp(freq,self.frequencies,self.load_max_gain)
        g_l_norm = gain/g_l_max
        s11 = np.interp(freq,self.frequencies,self.transistor.complex[0,0])
        s22 = np.interp(freq,self.frequencies,self.transistor.complex[1,1])

        if source_or_load == "source":
            center = (g_s_norm*np.conjugate(s11))/(1-np.abs(s11)**2*(1-g_s_norm))
            radius = (np.sqrt(1-g_s_norm)*(1-np.abs(s11)**2))/(1-np.abs(s11)**2*(1-g_s_norm))
        
        if source_or_load == "load":
            center = (g_l_norm*np.conjugate(s22))/(1-np.abs(s22)**2*(1-g_l_norm))
            radius = (np.sqrt(1-g_l_norm)*(1-np.abs(s22)**2))/(1-np.abs(s22)**2*(1-g_l_norm))

        min_gamma_mag = np.abs(center)-np.abs(radius)
        min_gamma_ang = np.atan2(np.imag(center),np.real(center))
        min_gamma = (min_gamma_mag*np.cos(min_gamma_ang) + 1j*min_gamma_mag*np.sin(min_gamma_ang))

        return center,radius,min_gamma

    
    def calc_transducer_impedance(self,freq):
        gamma_s = np.interp(freq,self.frequencies,self.transistor.complex[0,0])
        source_imp = 50*((-1-gamma_s)/(gamma_s-1))
        gamma_l = np.interp(freq,self.frequencies,self.transistor.complex[1,1])
        load_imp = 50*((-1-gamma_l)/(gamma_l-1))
        return source_imp,load_imp