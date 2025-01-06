import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import pdist
from matplotlib.patches import Circle

def particle_angle_analysis_v2(positions, dbond, bounds=(-55, 55), marker_radius=1, mode='center', particle_diameter=2.21):
    """
    Perform particle angle analysis on given positions and visualize the results.

    Parameters:
        positions (numpy.ndarray): Nx2 array of particle positions.
        threshold (float): Distance threshold for grouping clusters.
        bounds (tuple): Bounds for the plot (xmin, xmax, ymin, ymax).
        marker_radius (float): Radius of the marker used for the particles.
    """
    N = positions.shape[0]  # Number of particles

    # Adjust threshold based on mode
    if mode == 'surface':
        dbond -= particle_diameter

    # Initialize animation
    plt.figure(figsize=(8, 8))
    plt.axis([bounds[0], bounds[1], bounds[0], bounds[1]])
    plt.gca().set_aspect('equal', adjustable='box')

    # Initialize variables
    groups = []  # List to store groups of particles
    colors = np.full(N, 'b', dtype=str)  # Initialize all particles as blue

    # Perform linkage
    distances = pdist(positions)
    linkage_matrix = linkage(distances, method='complete')

    # Cut dendrogram at dbond distance
    clusters = fcluster(linkage_matrix, t=dbond, criterion='distance')

    # Create groups of three particles
    for i in range(N - 2):
        for j in range(i + 1, N - 1):
            for k in range(j + 1, N):
                if clusters[i] == clusters[j] == clusters[k]:
                    groups.append([i, j, k])

    # Calculate angle between lines and color particles
    for group in groups:
        middle, bonded1, bonded2 = group
        line1 = np.append(positions[middle] - positions[bonded1], 0)
        line2 = np.append(positions[middle] - positions[bonded2], 0)
        angle = np.degrees(np.arctan2(np.linalg.norm(np.cross(line1, line2)), np.dot(line1, line2)))

        # Color based on bond angle
        if 70 < bond_angle < 140:
            colors[i] = 'g'  # Open link configuration
            colors[j] = 'g'
            colors[k] = 'g'
        elif 50 < bond_angle < 70:
            colors[i] = 'r'  # Closed link configuration
            colors[j] = 'r'
            colors[k] = 'r'
        elif 140 < angle < 180:
            colors[i] = 'y'  # Stretched link configuration
            colors[j] = 'y'
            colors[k] = 'y'

    # Draw particles
    for i in range(N):
        circle = Circle((positions[i, 0], positions[i, 1]), radius=marker_radius, edgecolor='black', facecolor=colors[i], linewidth=1)
        plt.gca().add_patch(circle)

    plt.title('Particle Angles Analysis (v2)')
    plt.xlabel('X Position')
    plt.ylabel('Y Position')
    plt.show()