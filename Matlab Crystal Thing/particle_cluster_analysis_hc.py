import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, fcluster



def plot_hierarchical_clustering(positions, threshold=3, bounds=(-55, 55), marker_size=2):
    """
    Perform hierarchical clustering on given positions and visualize the results.

    Parameters:
        positions (numpy.ndarray): Nx2 array of particle positions.
        threshold (float): Distance threshold for grouping clusters.
        bounds (tuple): Bounds for the plot (xmin, xmax, ymin, ymax).
        marker_size (float): Size of the marker used for the particles.
    """

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

    # Normalize the group sizes
    group_sizes = np.array(group_sizes)
    norm_group_sizes = (group_sizes - group_sizes.min()) / (group_sizes.max() - group_sizes.min())

    # Create a colormap (jet)
    cmap = plt.cm.jet

    # Plot the particles and color them according to group size
    plt.figure(figsize=(8, 8))
    plt.axis([bounds[0], bounds[1], bounds[0], bounds[1]])
    plt.gca().set_aspect('equal', adjustable='box')

    # Map the normalized sizes to colormap indices
    color_indices = (norm_group_sizes * 63).astype(int)

    for i, group in enumerate(groups):
        color = cmap(color_indices[i] / 63.0)
        for j in group:
            rect = plt.Rectangle((positions[j, 0] - marker_size / 2, positions[j, 1] - marker_size / 2),
                                 marker_size, marker_size, color=color, fill=True)
            plt.gca().add_patch(rect)

    # Add a colorbar
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=group_sizes.min(), vmax=group_sizes.max()))
    sm.set_array([])
    plt.colorbar(sm, label='Group Size')

    plt.title('Hierarchical Clustering Visualization')
    plt.xlabel('X Position')
    plt.ylabel('Y Position')
    plt.show()

# Example usage
# positions = np.load('positions.npy')
# plot_hierarchical_clustering(positions)
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
group_sizes = []

# Iterate through each group
unique_groups = np.unique(T)
for group_id in unique_groups:
    group_indices = np.where(T == group_id)[0]
    groups.append(group_indices)

    # Calculate the size of the group
    group_size = len(group_indices)
    group_sizes.append(group_size)

# Normalize the group sizes
group_sizes = np.array(group_sizes)
norm_group_sizes = (group_sizes - group_sizes.min()) / (group_sizes.max() - group_sizes.min())

# Create a colormap (jet)
cmap = plt.cm.jet

# Plot the particles and color them according to group size
plt.figure(figsize=(8, 8))
plt.axis([-55, 55, -55, 55])
plt.gca().set_aspect('equal', adjustable='box')

# Map the normalized sizes to colormap indices
color_indices = (norm_group_sizes * 63).astype(int)

for i, group in enumerate(groups):
    color = cmap(color_indices[i] / 63.0)
    for j in group:
        rect = plt.Rectangle((positions[j, 0] - 1, positions[j, 1] - 1), 2, 2, color=color, fill=True)
        plt.gca().add_patch(rect)

# Add a colorbar
sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=group_sizes.min(), vmax=group_sizes.max()))
sm.set_array([])
plt.colorbar(sm, label='Group Size')

plt.title('Hierarchical Clustering Visualization')
plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.show()

