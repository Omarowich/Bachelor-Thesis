import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import pdist
from matplotlib.patches import Rectangle

def particle_angle_analysis_hc(positions, threshold=3.5, bounds=(-55, 55)):
    """
    Perform particle angle analysis on given positions and visualize the results.

    Parameters:
        positions (numpy.ndarray): Nx2 array of particle positions.
        threshold (float): Distance threshold for grouping clusters.
        bounds (tuple): Bounds for the plot (xmin, xmax, ymin, ymax).
    """
    N = positions.shape[0]  # Number of particles

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

    # Cut dendrogram at threshold distance
    clusters = fcluster(linkage_matrix, t=threshold, criterion='distance')

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
        if 140 <= angle <= 180:
            colors[group] = 'r'  # Color the three particles red

    # Draw particles
    for i in range(N):
        rect = Rectangle((positions[i, 0] - 0.5, positions[i, 1] - 0.5), 1, 1,
                         edgecolor='black', facecolor=colors[i], linewidth=1)
        plt.gca().add_patch(rect)

    plt.title('Particle Grouping and Coloring by Angles')
    plt.xlabel('X Position')
    plt.ylabel('Y Position')
    plt.show()
