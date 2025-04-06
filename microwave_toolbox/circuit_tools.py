import numpy as np
import cmath
import os
from . import system_tools as st
from . import plotting_tools


class rf_amplifier():

    def __init__(self, s2p_in: st.network):
        #initialize basic variables
        self.type = "Amplifier"
        self.sub_type = "None"
        self.z_reference = 50
        self.transistor = s2p_in
        self.frequencies = s2p_in.frequencies
        self.g_s_max_gain = [1/(1-abs(x)**2) for x in self.transistor.complex[0][0]]
        self.gamma_s_max_gain = [np.conjugate(x) for x in self.transistor.complex[0][0]]
