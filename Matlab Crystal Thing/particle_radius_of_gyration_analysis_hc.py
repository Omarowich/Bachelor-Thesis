import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, fcluster
from matplotlib.patches import Circle

def particle_radius_of_gyration_analysis_hc(positions, threshold=3.1, bounds=(-50, 50), marker_radius=1):
    """
    Perform hierarchical clustering, calculate the radius of gyration for each group,
    and visualize the particles with colors corresponding to the radius of gyration.

    Parameters:
        positions (numpy.ndarray): Nx2 array of particle positions.
        threshold (float): Distance threshold for grouping clusters.
        bounds (tuple): Bounds for the plot (xmin, xmax, ymin, ymax).
        marker_radius (float): Radius of the marker used for the particles.
    """
    # Perform hierarchical clustering
    Z = linkage(positions, method='single')
    T = fcluster(Z, t=threshold, criterion='distance')

    # Initialize groups and radii
    groups = []
    group_radii = []

    # Iterate through each unique group
    unique_groups = np.unique(T)
    for group_id in unique_groups:
        group = np.where(T == group_id)[0]
        groups.append(group)

        # Calculate the center of mass
        center_of_mass = np.mean(positions[group], axis=0)

        # Calculate deviations from center of mass
        deviations = positions[group] - center_of_mass

        # Calculate the radius of gyration
        radius = np.sqrt(np.mean(np.sum(deviations ** 2, axis=1)))
        group_radii.append(radius)

    # Normalize group radii
    group_radii = np.array(group_radii)
    norm_group_radii = (group_radii - group_radii.min()) / (group_radii.max() - group_radii.min())

    # Create a colormap
    cmap = plt.cm.jet
    color_indices = (norm_group_radii * 63).astype(int)  # Map normalized radii to colormap indices

    # Plot particles
    fig, ax = plt.subplots(figsize=(8, 8))  # Define ax here
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlim(bounds[0], bounds[1])
    ax.set_ylim(bounds[0], bounds[1])

    for i, group in enumerate(groups):
        color = cmap(color_indices[i] / 63.0)
        for particle in group:
            circle = Circle(
                (positions[particle, 0], positions[particle, 1]),
                radius=marker_radius, color=color, fill=True
            )
            ax.add_patch(circle)

    # Add colorbar
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=group_radii.min(), vmax=group_radii.max()))
    sm.set_array([])
    plt.colorbar(sm, ax=ax, label='Normalized Radius of Gyration')

    # Add plot title and labels
    ax.set_title('Particle Clustering and Radius of Gyration')
    ax.set_xlabel('X Position')
    ax.set_ylabel('Y Position')
    plt.show()