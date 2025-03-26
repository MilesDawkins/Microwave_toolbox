import numpy as np
import cmath
import os
import matplotlib.pyplot as plot

def ArrayFactor(ElementArray, Freq):
    
    arrayFactor = np.ones((360, 95))
    Lambda = 3e8 / Freq

    for theta in range(95):
        for phi in range(360):                                                                                                      # For all theta/phi positions
            elementSum = 1e-9 + 0j

            for element in ElementArray:                                                                                            # Summation of each elements contribution at theta/phi position.
                relativePhase = CalculateRelativePhase(element, Lambda, np.radians(theta), np.radians(phi))                     
                elementSum += element[3] * np.e ** ((relativePhase + element[4]) * 1j)                                            # Element contribution = Amp * e^j(Phase + Phase Weight)

            arrayFactor[phi][theta] = elementSum.real

    return arrayFactor

  
def CalculateRelativePhase(Element, Lambda, theta, phi):

    phaseConstant = (2 * np.pi / Lambda)

    xVector = Element[0] * np.sin(theta) * np.cos(phi)
    yVector = Element[1] * np.sin(theta) * np.sin(phi)
    zVector = Element[2] * np.cos(theta)

    phaseOfIncidentWaveAtElement = phaseConstant * (xVector + yVector + zVector)

    return phaseOfIncidentWaveAtElement