import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, fcluster
from matplotlib.colors import LinearSegmentedColormap

# Load positions (assuming positions is saved as an Nx2 numpy array in positions.npy)
positions = np.load('positions.npy')

# Set the distance threshold for grouping
threshold = 3

# Perform hierarchical clustering
Z = linkage(positions, method='single')

# Create the groups from the linkage matrix
T = fcluster(Z, t=threshold, criterion='distance')

# Initialize groups and group sizes
groups = []
group_radii = []

# Iterate through each group
unique_groups = np.unique(T)
for group_id in unique_groups:
    group_indices = np.where(T == group_id)[0]
    groups.append(group_indices)

    # Calculate the center of mass of the group
    center_of_mass = positions[group_indices].mean(axis=0)

    # Calculate the deviation of each particle from the center of mass
    deviation = positions[group_indices] - center_of_mass

    # Calculate the radius of gyration for the group
    radius = np.sqrt(np.mean(np.sum(deviation**2, axis=1)))
    group_radii.append(radius)

# Normalize the group radii
group_radii = np.array(group_radii)
norm_group_radii = (group_radii - group_radii.min()) / (group_radii.max() - group_radii.min())

# Create a custom colormap (red-blue)
def redblue():
    return LinearSegmentedColormap.from_list('redblue', [(0, 'red'), (1, 'blue')], N=64)

cmap = redblue()

# Plot the particles and color them according to group radius
plt.figure(figsize=(8, 8))
plt.axis([-55, 55, -55, 55])
plt.gca().set_aspect('equal', adjustable='box')

# Map the normalized radii to colormap indices
color_indices = (norm_group_radii * 63).astype(int)

for i, group in enumerate(groups):
    color = cmap(color_indices[i])
    for j in group:
        circle = plt.Circle((positions[j, 0], positions[j, 1]), 1, color=color, fill=True)
        plt.gca().add_patch(circle)

# Add a colorbar
sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=group_radii.min(), vmax=group_radii.max()))
sm.set_array([])
plt.colorbar(sm, label='Group Radius')

plt.title('Hierarchical Clustering Visualization')
plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.show()
