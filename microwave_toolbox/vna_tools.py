import numpy as np
from numpy.polynomial import Polynomial
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from . import system_tools as st

def custom_cal_kit_polynomial_calc(net: st.network, type=None):
    # OPEN CALCULATIONS
    if type == "open":
        s11 = net.complex[0, 0]
        freqs = np.array(net.frequencies)
        

        # Calculate delay from unwrapped S11 phase
        phase_rad = np.unwrap(np.angle(s11))
        dphi_df = np.gradient(phase_rad, freqs)
        delay_s = -dphi_df / (4 * np.pi)
        delay_ps = delay_s * 1e12
        avg_delay_ps = np.mean(delay_ps)

        # De-embed delay from S11
        tau = avg_delay_ps * 1e-12  # delay in seconds
        s11_corr = s11 * np.exp(1j * 2 * np.pi * freqs * tau)

        # Convert to Y11
        Z0 = 50
        gamma = s11_corr
        Y11 = (1 - gamma) / (1 + gamma) / Z0

        # Calculate C(f) from imag(Y11)
        omega = 2 * np.pi * freqs
        C = np.imag(Y11) / omega

        # Fit 3rd-order polynomial to C(f)
        p = Polynomial.fit(freqs, C, 3)

        coeffs = p.convert().coef
        return coeffs, avg_delay_ps


    # SHORT CALCULATIONS
    elif type == "short":
        s11 = net.complex[0, 0]
        freqs = np.array(net.frequencies)
        

        # Calculate delay from unwrapped S11 phase
        phase_rad = np.unwrap(np.angle(s11))
        dphi_df = np.gradient(phase_rad, freqs)
        delay_s = -dphi_df / (4 * np.pi)
        delay_ps = delay_s * 1e12
        avg_delay_ps = np.mean(delay_ps)

        # De-embed delay from S11
        tau = avg_delay_ps * 1e-12
        s11_corr = s11 * np.exp(1j * 2 * np.pi * freqs * tau)

        # Convert to Z11
        Z0 = 50
        gamma = s11_corr
        Z11 = Z0 * (1 + gamma) / (1 - gamma)

        # Calculate L(f) from imag(Z11)
        omega = 2 * np.pi * freqs
        L = np.imag(Z11) / omega

        # Fit 3rd-order polynomial to L(f)
        p = Polynomial.fit(freqs, L, 3)

        coeffs = p.convert().coef
        return coeffs, avg_delay_ps


    # LOAD CALCULATIONS
    elif type == "load":
        freq = np.array(net.frequencies)  # in Hz
        s11 = net.complex[0,0]

        # Load model: R + jωL - j/(ωC)
        def load_model(freq, R, L, C):
            omega = 2 * np.pi * freq
            Z = R + 1j * omega * L - 1j / (omega * C)
            return (Z - 50) / (Z + 50)

        def fit_func(freq, R, L, C):
            s11_model = load_model(freq, R, L, C)
            return np.concatenate([np.real(s11_model), np.imag(s11_model)])

        # Prepare data for fitting
        ydata = np.concatenate([np.real(s11), np.imag(s11)])
        p0 = [50, 1e-9, 1e-12]  # Initial guesses

        # Fit to extract R, L, C
        popt, _ = curve_fit(fit_func, freq, ydata, p0=p0)
        R, L, C = popt

        # Delay extraction from measured S11 phase
        phase_rad = np.unwrap(np.angle(s11))
        dphi_df = np.gradient(phase_rad, freq)
        delay_s = -dphi_df / (4 * np.pi)
        delay_ps = delay_s * 1e12
        avg_delay_ps = np.mean(delay_ps)

        # Impedance offset calculation
        Z_load = 50 * (1 + s11) / (1 - s11)
        Z_offset = np.mean(Z_load)  # Complex average impedance


        return  Z_offset, avg_delay_ps

    else:
        raise ValueError("type must be one of: 'open', 'short', or 'load'")