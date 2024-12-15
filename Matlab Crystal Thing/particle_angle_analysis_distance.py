import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform
from matplotlib.patches import Rectangle

# Load positions (assuming positions is saved as an Nx2 numpy array in positions_v2.npy)
positions = np.load('positions_v2.npy')
N = positions.shape[0]  # Number of particles

# Set the distance threshold for grouping
threshold = 3

# Initialize animation
plt.figure(figsize=(8, 8))
plt.axis([-55, 55, -55, 55])
plt.gca().set_aspect('equal', adjustable='box')

# Find the distance between each particle
distances = squareform(pdist(positions))

# Find the groups of three particles
groups = []
for i in range(N):
    for j in range(i + 1, N):
        if distances[i, j] <= threshold:
            for k in range(j + 1, N):
                if distances[i, k] <= threshold:
                    groups.append([i, j, k])

# Initialize particle colors
colors = np.full(N, 'b', dtype=str)

# Calculate the bonding angles and color the particles
for group in groups:
    i, j, k = group
    # Find the bonding angle
    line1 = np.append(positions[j] - positions[i], 0)
    line2 = np.append(positions[k] - positions[i], 0)
    bond_angle = np.degrees(np.arctan2(np.linalg.norm(np.cross(line1, line2)), np.dot(line1, line2)))
    # If the angle is between 140 and 180 degrees
    if 140 <= bond_angle <= 180:
        colors[i] = 'r'
        colors[j] = 'r'
        colors[k] = 'r'

# Draw the particles
for i in range(N):
    rect = Rectangle((positions[i, 0] - 1, positions[i, 1] - 1), 2, 2,
                     edgecolor='black', facecolor=colors[i], linewidth=1)
    plt.gca().add_patch(rect)

plt.title('Particle Grouping and Coloring by Angles')
plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.show()
