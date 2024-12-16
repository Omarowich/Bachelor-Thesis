import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, fcluster
from matplotlib.patches import Circle

def particle_cluster_analysis_hc(positions, threshold=3, bounds=(-55, 55), marker_radius=1):
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

    # Normalize the group sizes
    group_sizes = np.array(group_sizes)
    norm_group_sizes = (group_sizes - group_sizes.min()) / (group_sizes.max() - group_sizes.min())

    # Create a colormap (jet)
    cmap = plt.cm.jet

    # Plot the particles and color them according to group size
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlim(bounds[0], bounds[1])
    ax.set_ylim(bounds[0], bounds[1])

    # Map the normalized sizes to colormap indices
    color_indices = (norm_group_sizes * 63).astype(int)

    for i, group in enumerate(groups):
        color = cmap(color_indices[i] / 63.0)
        for j in group:
            circle = Circle((positions[j, 0], positions[j, 1]), radius=marker_radius, color=color, fill=True)
            ax.add_patch(circle)

    # Add a colorbar
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=group_sizes.min(), vmax=group_sizes.max()))
    sm.set_array([])
    plt.colorbar(sm, ax=ax, label='Group Size')

    ax.set_title('Particle Cluster Analysis by Hierarchical Clustering')
    ax.set_xlabel('X Position')
    ax.set_ylabel('Y Position')
    plt.show()