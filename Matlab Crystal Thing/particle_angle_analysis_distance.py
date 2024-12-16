import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform
from matplotlib.patches import Circle

def particle_angle_analysis_distance(positions, threshold=3, bounds=(-55, 55), marker_radius=1):
    """
    Perform particle angle analysis on given positions and visualize the results.

    Parameters:
        positions (numpy.ndarray): Nx2 array of particle positions.
        threshold (float): Distance threshold for grouping clusters.
        bounds (tuple): Bounds for the plot (xmin, xmax, ymin, ymax).
        marker_radius (float): Radius of the marker used for the particles.
    """
    N = positions.shape[0]  # Number of particles

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
        circle = Circle((positions[i, 0], positions[i, 1]), radius=marker_radius, edgecolor='black', facecolor=colors[i], linewidth=1)
        plt.gca().add_patch(circle)

    plt.title('Particle Angles Analysis (Distance)')
    plt.xlabel('X Position')
    plt.ylabel('Y Position')
    plt.show()