import numpy as np
import matplotlib.pyplot as plt

# Generate a sample 2D signal (e.g., a grayscale image)
image = np.zeros((64, 64))
image[20:40, 20:40] = 1  # Create a white square in the center

# Compute the 2D FFT
fft_image = np.fft.fft2(image)
print(fft_image)
# Shift the zero-frequency component to the center
fft_shifted = np.fft.fftshift(fft_image)

# Calculate magnitude spectrum for visualization
magnitude_spectrum = np.abs(fft_shifted)

# Display the original image and its FFT
plt.figure(figsize=(10, 5))

plt.subplot(121)
plt.imshow(image, cmap='gray')
plt.title('Original Image')

plt.subplot(122)
plt.imshow(np.log(magnitude_spectrum + 1), cmap='gray') #Logarithmic scaling to visualize the wide range of magnitudes
plt.title('FFT Magnitude Spectrum')

plt.show()

# Inverse FFT to reconstruct the image
ifft_image = np.fft.ifft2(fft_image)

# Verify reconstruction (check if the real part of the reconstructed image is close to the original)
np.allclose(image, np.real(ifft_image))