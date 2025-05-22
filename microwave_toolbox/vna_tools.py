
import numpy as np
from numpy.polynomial import Polynomial
import matplotlib.pyplot as plt
from . import system_tools as st


def custom_cal_kit_polynomial_calc(net : st.network,type = None):
    # Load the Open standard

    #OPEN CALCUILATIONS
    if type =="open":
        # Convert to Y-parameters and extract imaginary part of Y11
        c = np.imag(net.y[0,0]) / (2 * np.pi * np.array(net.frequencies))  # Capacitance at each freq
        # Fit 3rd-order polynomial to C(f)
        p = Polynomial.fit(np.array(net.frequencies), c, 3)  # Polynomial fit in GHz

    #SHORT CALCULATIONS
    if type == "short":
        # Convert to Z-parameters and extract imaginary part of Y11
        l = np.imag(net.impedance[0,0]) / (2 * np.pi * np.array(net.frequencies))  # Capacitance at each freq
        # Fit 3rd-order polynomial to L(f)
        p = Polynomial.fit(np.array(net.frequencies), l, 3)  # Polynomial fit in GHz


    # Get coefficients (standard basis)
    coeffs = p.convert().coef  # a0, a1, a2, a3

    #CALCULATION OF OFFSET DELAY
    freqs_Hz = np.array(net.frequencies)
    freqs_GHz = freqs_Hz / 1e9

    # Extract S11 and unwrap phase
    
    phase_rad = np.unwrap(np.angle(net.complex[0,0]))
    # Calculate delay from phase slope
    dphi_df = np.gradient(phase_rad, freqs_Hz)
    delay_s = -dphi_df / (4 * np.pi)  # round-trip delay factor
    delay_ps = delay_s * 1e12

    # Select frequency range for averaging
    band = (freqs_GHz >= np.min(net.frequencies)/1E9) & (freqs_GHz <= np.max(net.frequencies)/1E9)
    avg_delay_ps = np.mean(delay_ps[band])



    return coeffs,avg_delay_ps

