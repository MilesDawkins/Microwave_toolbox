import numpy as np
import cmath
import os
import matplotlib.pyplot as plot
from . import antenna_tools as at

class element_array:


    def __init__(self, element : at.antenna, element_coor : list, weights = None, phases = None):
        self.element = element
        self.element_coor = element_coor
        self.array_factor = np.ones((360, 180))
        self.num_elements = len(element_coor)

        if weights is not None:
            self.weights = weights
        else:
            self.weights = np.ones(self.num_elements)

        if phases is not None:
            self.phases = phases
        else:
            self.phases = np.zeros(self.num_elements)
        
        
        
        return

    def calc_array_factor(self, Freq):
        
        theta = np.linspace(0,90,)
        Lambda = 3e8 / Freq

        for theta in range(180):
            for phi in range(360):                                                                                                      # For all theta/phi positions
                element_sum = 1e-9 + 0j
                for element in range(self.num_elements):                                                                                            # Summation of each elements contribution at theta/phi position.
                    wave_phase = self.calc_wave_phase(self.element_coor[element], Lambda, np.radians(theta), np.radians(phi))                     
                    element_sum += self.weights[element] * np.e ** ((wave_phase + self.phases[element]) * 1j)                                            # Element contribution = Amp * e^j(Phase + Phase Weight)
                self.array_factor[phi][theta] = element_sum.real


    
    def calc_wave_phase(self,Element:list, Lambda, theta, phi):

        phaseConstant = (2 * np.pi / Lambda)

        xVector = Element[0] * np.sin(theta) * np.cos(phi)
        yVector = Element[1] * np.sin(theta) * np.sin(phi)
        zVector = Element[2] * np.cos(theta)

        element_wave_phase = phaseConstant * (xVector + yVector + zVector)

        return element_wave_phase