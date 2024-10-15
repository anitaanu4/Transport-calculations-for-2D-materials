#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 17:26:30 2024

@author: anu
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.colors import LinearSegmentedColormap


# Initialize empty arrays for each column
kx = []
ky = []
weight = []
energy = []

# Open the file
with open('/Users/anu/Dropbox/FGT/Fe5GaTe2/kreolved/monolayer/F5GT_mono_TRC_down', 'r') as file:
#with open('AuFGaT4.TRC.k.down', 'r') as file:
    # Read the file line by line
    for line in file:
        # Split each line into columns based on whitespace delimiter
        columns = line.strip().split()
        
        # Store each column into respective arrays
        kx.append(columns[0])
        ky.append(columns[1])
        weight.append(columns[3])
        energy.append(columns[4])
        
        
kxsort=[]
kysort=[]
weightsort=[]
energysort=[]

        
c=energy[2] #change it as per your file

for i in range(len(energy)):
    if energy[i] == c:
        kxsort.append(kx[i])
        kysort.append(ky[i])
        weightsort.append(weight[i])
        energysort.append(energy[i])
    if energy[i] == c:
        kxsort.append(kx[i])
        kysort.append(ky[i])
        weightsort.append(weight[i])
        energysort.append(energy[i])


# Convert the lists to numpy arrays
x = np.array(kxsort, dtype=np.float64)
y = np.array(kysort, dtype=np.float64)

a1 = np.array([4.07, 0, 0])
a2 = np.array([-2.035, 3.5247235421, 0])
V = np.dot(a1, np.cross(a2, np.array([0, 0, 1])))
b1 = (2 * np.pi / V) * np.cross(a2, np.array([0, 0, 1]))
b2 = (2 * np.pi / V) * np.cross(np.array([0, 0, 1]), a1)

#points = [
#    [-0.5555407936330121, -1.20579102258489e-11],
#    [-0.2777703968252901, -0.4811124401196853],
#    [0.2777703968252901, -0.4811124401196853],
#    [0.5555407936330121, 1.2058132270453825e-11],
#    [0.2777703968252901, 0.4811124401196853],
#    [-0.2777703968252901, 0.4811124401196853],
#    [-0.5555407936330121, -1.20579102258489e-11],
#] #FGT3

#points = [
#    [-0.5654611662864423, 0.0],
#    [-0.28273058316383376, -0.48970373484573504],
#    [0.28273058316383376, -0.4897037348457351],
#    [0.5654611662864423, 0.0],
#    [0.28273058316383376, 0.4897037348457351],
#   [-0.28273058316383376, 0.4897037348457351],
#    [-0.5654611662864423, 0.0],
#] #FGT4-monolayer

points = [
    [-0.5505595202621936, 1.1842860025979007e-11],
    [-0.27527976012934874, -0.4767985308434421],
    [0.27527976012934874, -0.4767985308434421],
    [0.5505595202621936, 1.1842860025979007e-11],
    [0.28273058316383376, 0.4897037348457351],
    [-0.27527976012934874, 0.4767985308434421],
    [-0.5505595202621936, 1.1842860025979007e-11],
] #FGT4-monolayer


# Extract x and y coordinates
x_bz = [point[0] for point in points]
y_bz = [point[1] for point in points]

# Plot the points
#plt.scatter(x_bz, y_bz)
# Function to convert scientific notation string to float and format it
def convert(scientific_str):
    # Replace 'D' with 'e' to conform to Python's scientific notation format
    scientific_str = scientific_str.replace('D', 'e')
    try:
        # Convert the modified string to a floating-point number
        return float(scientific_str)
    except ValueError:
        # Handle non-numeric values (e.g., 'NaN', 'Inf') by returning a placeholder value
        return np.nan  # or any other suitable placeholder value

# Convert each element in the array and format it
z = [convert(elem) for elem in weightsort]



plt.figure(figsize=(7, 6.1))
# Create a continuous color plot
contour = plt.tricontourf(x, y, z, cmap='inferno')
plt.clim(0, 1.05)
#plt.colorbar(ticks=[0, 0.5, 0.7, 1.05])
# Plot the set of points in red on top of the color map
#plt.scatter(x_bz, y_bz, color='w', label='Points')
plt.plot(x_bz, y_bz, color='white', linewidth=3, linestyle='-')
#cbar = plt.colorbar(contour)
#cbar.set_clim(0, 1.05) 
# Add labels and title
#plt.xlabel('Kx')
#plt.ylabel('Ky')
#plt.title('T(E, Kx, Ky)')

# Create a colorbar using the mappable object returned by tricontourf
#plt.colorbar(contour, label='Energy')
# Create a color bar with a label
#cbar = plt.colorbar(contour)
#cbar.set_clim(0, 2)
#cbar.set_ticks([0, 1, 2])
# Set font properties for the color bar
#cbar.ax.yaxis.set_tick_params(labelsize=14)  # Adjust label size if needed
#cbar.ax.yaxis.set_tick_params(labelfamily='helvetica')  # Set font family to Helvetica
# Set color bar range


# Hide the x and y ticks
#plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
#plt.tick_params(axis='y', which='both', left=False, right=False, labelleft=False)
## Set the DPI for high quality
#plt.plot(0, 0, marker='o', markersize=6, color='white') 
plt.rcParams['font.family'] = 'Helvetica'
plt.colorbar(ticks=[0, 0.15, 0.30, 0.45, 0.60, 0.75, 0.9, 1.05])
plt.rcParams['font.weight'] = 'bold'
plt.savefig('/Users/anu/Dropbox/FGT/Fe5GaTe2/kreolved/monolayer/spin-dn-new_paper.png', dpi=1200)  # Save the figure with 300 DPI
# Show the plot
plt.show()

