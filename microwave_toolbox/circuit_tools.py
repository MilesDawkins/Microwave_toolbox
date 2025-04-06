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
        self.g_s_max_gain = [1/(1-abs(x)**2) for x in self.transistor.complex[0][0]]
        self.gamma_s_max_gain = [np.conjugate(x) for x in self.transistor.complex[0][0]]
        self.g_l_max_gain = [1/(1-abs(x)**2) for x in self.transistor.complex[1][1]]
        self.gamma_l_max_gain = [np.conjugate(x) for x in self.transistor.complex[1][1]]
        self.max_z0_transducer_gain = [abs(x)**2 for x in self.transistor.complex[1][0]]
        self.max_transducer_gain = [x + y + z for x,y,z in zip(self.g_l_max_gain,self.g_s_max_gain,self.max_z0_transducer_gain)]
    
    def calc_gain_circle(self,log_gain,freq):
        gain = 10**(log_gain/10)
        g_s_max = np.interp(freq,self.frequencies,self.g_s_max_gain)
        g_s_norm = gain/g_s_max
        g_l_max = np.interp(freq,self.frequencies,self.g_l_max_gain)
        g_l_norm = gain/g_l_max
        s11 = np.interp(freq,self.frequencies,self.transistor.complex[0][0])
        s22 = np.interp(freq,self.frequencies,self.transistor.complex[1][1])

        source_center = (g_s_norm*np.conjugate(s11))/(1-np.abs(s11)**2*(1-g_s_norm))
        load_center = (g_l_norm*np.conjugate(s22))/(1-np.abs(s22)**2*(1-g_l_norm))

        source_radius = (np.sqrt(1-g_s_norm)*(1-np.abs(s11)**2))/(1-np.abs(s11)**2*(1-g_s_norm))
        load_radius = (np.sqrt(1-g_l_norm)*(1-np.abs(s22)**2))/(1-np.abs(s22)**2*(1-g_l_norm))

        min_gamma_mag_s = np.abs(source_center)-np.abs(source_radius)
        min_gamma_ang_s = np.atan(np.imag(source_center)/np.real(source_center))
        if np.imag(source_center) < 0:
            min_gamma_ang_s = min_gamma_ang_s + np.pi
        print(min_gamma_ang_s)
        if min_gamma_ang_s < 0:
            min_gamma_ang_s = min_gamma_ang_s + np.pi
        min_gamma_source = (min_gamma_mag_s*np.cos(min_gamma_ang_s) + 1j*min_gamma_mag_s*np.sin(min_gamma_ang_s))

        min_gamma_mag_l = np.abs(load_center)-np.abs(load_radius)
        min_gamma_ang_l = np.atan(np.imag(load_center)/np.real(load_center))
        if np.imag(load_center) < 0:
            min_gamma_ang_l = min_gamma_ang_l + np.pi
        if min_gamma_ang_l < 0:
            min_gamma_ang_l = min_gamma_ang_l + np.pi
        min_gamma_load = (min_gamma_mag_l*np.cos(min_gamma_ang_l) + 1j*min_gamma_mag_l*np.sin(min_gamma_ang_l))

        return source_center,source_radius,load_center,load_radius, min_gamma_source, min_gamma_load
    
    def calc_transducer_impedance(self,freq):
        gamma_s = np.interp(freq,self.frequencies,self.transistor.complex[0][0])
        source_imp = 50*((-1-gamma_s)/(gamma_s-1))
        gamma_l = np.interp(freq,self.frequencies,self.transistor.complex[1][1])
        load_imp = 50*((-1-gamma_l)/(gamma_l-1))
        return source_imp,load_imp