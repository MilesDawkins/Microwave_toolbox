import numpy as np
import cmath
import os
from . import system_tools
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
    def __init__(self, s2p_in: system_tools.network):
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
    


class attenuator():
    def __init__(self,zo,attenuation,config = None,freqs_in = None):
        # create class instance globals
        self.sub_type = "attenuator"
        self.zo=zo
        self.attenuation = attenuation

        if  config != None:
            self.config = config
        else:
            self.config = "pi"

        
        # calculate initial attenuator parameters
        self.attenuator_calc()
    
        if freqs_in is not None:
            self.frequencies = freqs_in
            self.create_network(freqs_in)


    def attenuator_calc(self):
        if self.config == "pi":
            self.shunt_r = self.zo*((10**(self.attenuation/20)+1)/(10**(self.attenuation/20)-1))
            self.series_r = self.zo/2*((10**(self.attenuation/10)-1)/(10**(self.attenuation/20)))
        elif self.config == "tee":
            self.series_r = self.zo*((10**(self.attenuation/20)-1)/(10**(self.attenuation/20)+1))
            self.shunt_r = 2*self.zo*((10**(self.attenuation/20))/(10**(self.attenuation/10)-1))


    def create_network(self,freqs):
        self.network = system_tools.network(num_ports=2,frequencies=freqs,format='ABCD')
        series_y = 1/(self.series_r)
        shunt_y = 1/(self.shunt_r)
        
        if self.config == "pi":

            #A
            self.network.file_data[0][0]=1+shunt_y/series_y

            #B
            self.network.file_data[0][1]=1/series_y

            #C
            self.network.file_data[1][0]=2*shunt_y+shunt_y**2/series_y

            #D
            self.network.file_data[1][1]=1+shunt_y/series_y
        
        elif self.config == "tee":

            #A
            self.network.file_data[0][0]=1+self.series_r/self.shunt_r

            #B
            self.network.file_data[0][1]=2*self.series_r+self.series_r**2/self.shunt_r

            #C
            self.network.file_data[1][0]=1/self.shunt_r

            #D
            self.network.file_data[1][1]=1+self.series_r/self.shunt_r







class resistor():
    def __init__(self,resistance,config = None,freqs_in = None):
        # create class instance globals
        self.sub_type = "resistor"
        self.resistance = resistance

        if  config != None:
            self.config = config
        else:
            self.config = "series"
    
        if freqs_in is not None:
            self.frequencies = freqs_in
            self.create_network(freqs_in)

    def create_network(self,freqs):
        self.network = system_tools.network(num_ports=2,frequencies=freqs,format='ABCD')
        
        if self.config == "series":

            #A
            self.network.file_data[0][0]=1

            #B
            self.network.file_data[0][1]=self.resistance

            #C
            self.network.file_data[1][0]=0

            #D
            self.network.file_data[1][1]=1
        
        elif self.config == "shunt":

            #A
            self.network.file_data[0][0]=1

            #B
            self.network.file_data[0][1]=0

            #C
            self.network.file_data[1][0]=1/self.resistance

            #D
            self.network.file_data[1][1]=1


class capacitor():
    def __init__(self,capacitance,config = None,freqs_in = None):
        # create class instance globals
        self.sub_type = "capacitor"
        self.capacitance = capacitance

        if  config != None:
            self.config = config
        else:
            self.config = "series"
    
        if freqs_in is not None:
            self.frequencies = freqs_in
            self.create_network(freqs_in)

    def create_network(self,freqs):
        self.network = system_tools.network(num_ports=2,frequencies=freqs,format='ABCD')
        
        if self.config == "series":

            #A
            self.network.file_data[0][0]=1

            #B
            self.network.file_data[0][1]=-1j*1/(2*np.pi*freqs*self.capacitance)

            #C
            self.network.file_data[1][0]=0

            #D
            self.network.file_data[1][1]=1
        
        elif self.config == "shunt":

            #A
            self.network.file_data[0][0]=1

            #B
            self.network.file_data[0][1]=0

            #C
            self.network.file_data[1][0]=1/(-1j*1/(2*np.pi*freqs*self.capacitance))

            #D
            self.network.file_data[1][1]=1


class inductor():
    def __init__(self,inductance,config = None,freqs_in = None):
        # create class instance globals
        self.sub_type = "inductor"
        self.inductance = inductance

        if  config != None:
            self.config = config
        else:
            self.config = "series"
    
        if freqs_in is not None:
            self.frequencies = freqs_in
            self.create_network(freqs_in)

    def create_network(self,freqs):
        self.network = system_tools.network(num_ports=2,frequencies=freqs,format='ABCD')
        
        if self.config == "series":

            #A
            self.network.file_data[0][0]=1

            #B
            self.network.file_data[0][1]=1j*2*np.pi*freqs*self.inductance

            #C
            self.network.file_data[1][0]=0

            #D
            self.network.file_data[1][1]=1
        
        elif self.config == "shunt":

            #A
            self.network.file_data[0][0]=1

            #B
            self.network.file_data[0][1]=0

            #C
            self.network.file_data[1][0]=1/(1j*2*np.pi*freqs*self.inductance)

            #D
            self.network.file_data[1][1]=1

class transformer():
    def __init__(self,ratio,freqs_in = None):
        # create class instance globals
        self.sub_type = "inductor"
        self.ratio = ratio

        if freqs_in is not None:
            self.frequencies = freqs_in
            self.create_network(freqs_in)

    def create_network(self,freqs):
        self.network = system_tools.network(num_ports=2,frequencies=freqs,format='ABCD')

        #A
        self.network.file_data[0][0]=self.ratio

        #B
        self.network.file_data[0][1]=0

        #C
        self.network.file_data[1][0]=0

        #D
        self.network.file_data[1][1]=1/self.ratio
        
    
        