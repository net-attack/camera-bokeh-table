import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Parameters
f = 40  # Focal length in mm
D = 2  # Subject distance in meters
CoC = 0.03 / 1000  # Circle of confusion in mm (converted to meters)
aperture_values = [1.7, 2, 2.8, 4, 5.6, 8, 11, 16, 22, 28]

# Functions to calculate depth of field
def hyperfocal_distance(f, N, CoC):
    return (f**2) / (N * CoC) / 1000 + f / 1000  # in meters

def near_point(H, D, f):
    return (H * D) / (H + (D - f / 1000))

def far_point(H, D, f):
    return (H * D) / (H - (D - f / 1000))

# Calculate depth of field for different aperture values
data = []
for N in aperture_values:
    H = hyperfocal_distance(f, N, CoC)
    D_n = near_point(H, D, f)
    D_f = far_point(H, D, f)
    DOF = D_f - D_n
    data.append([N, D_n, D_f, DOF])

# Create DataFrame
df = pd.DataFrame(data, columns=['Aperture', 'Near Point (m)', 'Far Point (m)', 'Depth of Field (DOF, m)'])

# Print table
print(df)

# Create plot
plt.figure(figsize=(10, 6))
plt.plot(df['Aperture'], df['Depth of Field (DOF, m)'], marker='o')
plt.xlabel('Aperture (f)')
plt.ylabel('Depth of Field (DOF, m)')
plt.title('Depth of Field (DOF) vs. Aperture')
plt.grid(True)
plt.gca().invert_xaxis()  # Aperture increases, DOF decreases
plt.savefig('dof_cheatsheet.png', dpi=300)
plt.show()
