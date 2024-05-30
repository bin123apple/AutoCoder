# Ensure matplotlib is installed: pip install matplotlib

import matplotlib.pyplot as plt
import numpy as np

# Create a range of values from 0 to 2pi
t = np.linspace(0, 2 * np.pi, 1000)

# Calculate x and y using heart shape formula
x = 16 * np.sin(t) ** 3
y = 13 * np.cos(t) - 5*np.cos(2*t) - 2*np.cos(3*t) - np.cos(4*t)

# Plot the heart shape
plt.plot(x, y, 'r')

# Optional: Adjust the plot for better visibility
plt.axis('equal')
plt.axis('off')

# Show the plot
plt.show()