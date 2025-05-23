import skrf as rf
import numpy as np
import matplotlib.pyplot as plt
from numpy.polynomial import Polynomial
import os

# Load the S1P file
script_directory = os.path.dirname(os.path.abspath(__file__))
file1 = os.path.join(script_directory,"diy_open2.s1p")
ntw = rf.Network(file1)


# Extract frequency and S11
freqs = ntw.f  # Hz
s11 = ntw.s[:, 0, 0]
freqs_GHz = freqs / 1e9

# Step 1: Estimate electrical delay from phase
phase_rad = np.unwrap(np.angle(s11))
dphi_df = np.gradient(phase_rad, freqs)
delay_s = -dphi_df / (4 * np.pi)
avg_delay_ps = np.mean(delay_s) * 1e12
tau = avg_delay_ps * 1e-12

# Step 2: De-embed delay
s11_corr = s11 * np.exp(1j * 2 * np.pi * freqs * tau)

# Step 3: Convert to admittance and extract capacitance
Z0 = 50
gamma = s11_corr
Y11 = (1 - gamma) / (1 + gamma) / Z0
omega = 2 * np.pi * freqs
C = np.imag(Y11) / omega  # Capacitance in F

# Step 4: Fit 3rd-order polynomial
p = Polynomial.fit(freqs_GHz, C, 3)
coeffs = p.convert().coef  # Standard basis

# Evaluate the fit
C_fit = p(freqs_GHz)

# Plot
plt.figure(figsize=(10, 6))
plt.plot(freqs_GHz, C * 1e15, label="Measured C(f)", alpha=0.8)
plt.plot(freqs_GHz, C_fit * 1e15, '--', label="Fitted Poly", linewidth=2)
plt.xlabel("Frequency (GHz)")
plt.ylabel("Capacitance (fF)")
plt.title("Capacitance vs Frequency (Open Standard)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# Print results
print("Polynomial Coefficients (femtofarads):")
for i, c in enumerate(coeffs):
    print(f"C{i} = {c * 1e15:.3f} fF")

print(f"\nEstimated Electrical Delay: {avg_delay_ps:.2f} ps")