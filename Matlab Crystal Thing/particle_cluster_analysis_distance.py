import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, fcluster
from matplotlib.patches import Circle

def particle_cluster_analysis_distance(positions, threshold=3.1, bounds=(-50, 50), marker_radius=1):
    """
    Perform hierarchical clustering on given positions and visualize the results.

    Parameters:
        positions (numpy.ndarray): Nx2 array of particle positions.
        threshold (float): Distance threshold for grouping clusters.
        bounds (tuple): Bounds for the plot (xmin, xmax, ymin, ymax).
        marker_radius (float): Radius of the marker used for the particles.
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

    # Plot the particles and color them according to group size
    plt.figure(figsize=(8, 8))
    plt.axis([bounds[0], bounds[1], bounds[0], bounds[1]])
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
            circle = Circle((positions[j, 0], positions[j, 1]), marker_radius, edgecolor=color, fill=False)
            plt.gca().add_patch(circle)

    plt.title('Particle Cluster Analysis by Distance')
    plt.xlabel('X Position')
    plt.ylabel('Y Position')
    plt.show()