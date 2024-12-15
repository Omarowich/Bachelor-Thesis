import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, fcluster
from matplotlib.patches import Circle

# Load positions (assuming positions is saved as an Nx2 numpy array in positions.npy)
positions = np.load('positions.npy')

# Set the distance threshold for grouping
threshold = 3.1

# Perform hierarchical clustering
Z = linkage(positions, method='single')

# Create the groups from the linkage matrix
T = fcluster(Z, t=threshold, criterion='distance')

# Initialize groups and group sizes
groups = []
group_sizes = []

# Iterate through each group
unique_groups = np.unique(T)
for group_id in unique_groups:
    group_indices = np.where(T == group_id)[0]
    groups.append(group_indices)

    # Calculate the size of the group
    group_size = len(group_indices)
    group_sizes.append(group_size)

# Plot the particles and color them according to group size
plt.figure(figsize=(8, 8))
plt.axis([-50, 50, -50, 50])
plt.gca().set_aspect('equal', adjustable='box')

for i, group in enumerate(groups):
    size = group_sizes[i]

    if size > 20:
        color = 'red'
    elif 15 <= size <= 20:
        color = 'yellow'
    elif 10 <= size <= 14:
        color = 'green'
    else:
        color = 'blue'

    for j in group:
        circle = Circle((positions[j, 0], positions[j, 1]), 1, edgecolor=color, fill=False)
        plt.gca().add_patch(circle)

plt.title('Hierarchical Clustering Visualization')
plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.show()
