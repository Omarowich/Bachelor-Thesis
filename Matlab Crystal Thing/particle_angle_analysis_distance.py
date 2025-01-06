import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform
from matplotlib.patches import Circle

def particle_angle_analysis_distance(positions, dbond, bounds=(-55, 55), marker_radius=1, mode='center', particle_diameter=2.21):
    """
    Perform particle angle analysis on given positions and visualize the results.

    Parameters:
        positions (numpy.ndarray): Nx2 array of particle positions.
        threshold (float): Distance threshold for grouping clusters.
        bounds (tuple): Bounds for the plot (xmin, xmax, ymin, ymax).
        marker_radius (float): Radius of the marker used for the particles.
        mode (str): 'center' for center-to-center distance, 'surface' for surface-to-surface distance.
        particle_diameter (float): Diameter of the particles.
    """
    N = positions.shape[0]  # Number of particles

    # Adjust threshold based on mode
    if mode == 'surface':
        dbond -= particle_diameter

    # Initialize animation
    plt.figure(figsize=(8, 8))
    plt.axis([bounds[0], bounds[1], bounds[0], bounds[1]])
    plt.gca().set_aspect('equal', adjustable='box')

    # Find the distance between each particle
    distances = squareform(pdist(positions))

    # Find the groups of three particles
    groups = []
    for i in range(N):
        for j in range(i + 1, N):
            if distances[i, j] <= dbond:
                for k in range(j + 1, N):
                    if distances[i, k] <= dbond:
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

    # Draw the particles
    for i in range(N):
        circle = Circle((positions[i, 0], positions[i, 1]), radius=marker_radius, edgecolor='black', facecolor=colors[i], linewidth=1)
        plt.gca().add_patch(circle)

    plt.title('Particle Angles Analysis (Distance)')
    plt.xlabel('X Position')
    plt.ylabel('Y Position')
    plt.show()