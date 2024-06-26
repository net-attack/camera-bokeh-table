import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Parameters
f = 40  # Focal length in mm
CoC = 0.03  # Circle of confusion in mm
aperture_values = [1.7, 2, 2.8, 4, 5.6, 8, 11, 16, 22, 28]
distances = [0.5, 1, 2, 5, 10, 20]  # Distances to subject in meters

# Functions to calculate depth of field
def hyperfocal_distance(f, N, CoC):
    return (f**2) / (N * CoC) / 1000 + f / 1000  # in meters

def near_point(H, D, f):
    return (H * D) / (H + (D - f / 1000))

def far_point(H, D, f):
    if D >= H:
        return np.inf  # When the distance is greater than or equal to hyperfocal distance, the far point is at infinity
    else:
        return (H * D) / (H - (D - f / 1000))

# Calculate near and far points for different aperture values and distances
near_data = []
far_data = []
for D in distances:
    near_row = []
    far_row = []
    for N in aperture_values:
        H = hyperfocal_distance(f, N, CoC)
        D_n = near_point(H, D, f)
        D_f = far_point(H, D, f)
        near_row.append(round(D_n,2))
        far_row.append(round(D_f,2))
    near_data.append(near_row)
    far_data.append(far_row)

# Create DataFrames
near_df = pd.DataFrame(near_data, columns=aperture_values, index=distances)
near_df.index.name = 'Distance (m)'
near_df.columns.name = 'Aperture (f)'

far_df = pd.DataFrame(far_data, columns=aperture_values, index=distances)
far_df.index.name = 'Distance (m)'
far_df.columns.name = 'Aperture (f)'

# Print tables
print("Near Points (m):")
print(near_df)
print("\nFar Points (m):")
print(far_df)

# Create combined plot for near and far points
plt.figure(figsize=(12, 8))
for D, near_values, far_values in zip(distances, near_data, far_data):
    plt.plot(aperture_values, near_values, marker='o', linestyle='-', label=f'Near Point at {D} m')
    plt.plot(aperture_values, far_values, marker='x', linestyle='--', label=f'Far Point at {D} m')

plt.xlabel('Aperture (f)')
plt.ylabel('Distance (m)')
plt.title('Near and Far Points vs. Aperture for Various Distances')
plt.legend()
plt.grid(True)

#plt.gca().invert_xaxis()  # Aperture increases, Near and Far Points adjust accordingly
#plt.yscale('log')  # Log scale to handle large values
plt.ylim(0,30)
plt.savefig('near_and_far_points_cheatsheet.png', dpi=300)
plt.show()


# Write tables and plot to Markdown file
with open('depth_of_field_example.md', 'w') as file:
    file.write("# EXAMPLE: Canon Canonet QL17 GIII\n")
    file.write("FL: 40mm, F/1.7-28, Distance:0.5-20m\n")
    
    file.write("### Near Points (m):\n\n")
    file.write(near_df.to_markdown())
    file.write("\n\n### Far Points (m):\n\n")
    file.write(far_df.to_markdown())
    file.write("\n\n### Plot:\n\n")
    file.write("![Near and Far Points Plot](near_and_far_points_cheatsheet.png)\n\n")
    file.write("**Near and Far Points Plot**\n\n")