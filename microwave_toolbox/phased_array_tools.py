import numpy as np
import cmath
import os
import matplotlib.pyplot as plot
from . import antenna_tools as at

class element_array:


    def __init__(self, element : at.antenna, element_coor : list, steps, weights = None, phases = None):
        self.element = element
        self.element_coor = element_coor
        self.array_factor = np.ones((steps, int(steps/2)),dtype=complex)
        self.num_elements = len(element_coor)

        if weights is not None:
            self.weights = weights
        else:
            self.weights = np.ones(self.num_elements)

        if phases is not None:
            self.phases = phases
        else:
            self.phases = np.zeros(self.num_elements)


    def calc_array_factor(self, Freq,steps):
        Lambda = 3e8 / Freq
        phi_a = np.linspace(0,2*np.pi,steps)
        theta_a = np.linspace(0,np.pi,int(steps/2))
        theta,phi = np.meshgrid(theta_a,phi_a)                                                                                  # For all theta/phi positions
        element_sum = 1e-9 + 0j * np.ones([len(phi_a),len(theta_a)])
        for element in range(self.num_elements):                                                                       # Summation of each elements contribution at theta/phi position.
            wave_phase = self.calc_wave_phase(self.element_coor[element], Lambda,theta, phi)                     
            element_sum += self.weights[element] * np.e ** ((wave_phase + self.phases[element]) * 1j)                  # Element contribution = Amp * e^j(Phase + Phase Weight)
        self.array_factor = element_sum


    
    def calc_wave_phase(self,ele_coor:list, Lambda, theta, phi):

        phaseConstant = (2 * np.pi / Lambda)

        xVector = ele_coor[0] * np.sin(theta) * np.cos(phi)
        yVector = ele_coor[1] * np.sin(theta) * np.sin(phi)
        zVector = ele_coor[2] * np.cos(theta)

        element_wave_phase = phaseConstant * (xVector + yVector + zVector)

        return element_wave_phase