import numpy as np
import cmath
import os
from . import system_tools as st
from . import plotting_tools


class amplifier():

    def __init__(self, s2p: st.network):
        self.type = "Amplifier"
        self.sub_type = "None"
        self.z_reference = 50
        self.reversed = False
        
    