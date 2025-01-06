import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform
from matplotlib.patches import Circle

def crystal_classifier(coordinates, neighbors_indices, angles, angle_threshold=5.0, dbond=2.21, bounds=(-55, 55), marker_radius=1, mode='center'):
    """
    Classify crystal structures based on particle positions and bond angles, then visualize the results.

    Parameters:
        coordinates (numpy.ndarray): Nx2 array of particle positions.
        neighbors_indices (list of lists): Indices of nearest neighbors for each particle.
        angles (list of lists): List of angles between particles.
        angle_threshold (float): Threshold for angle similarity.
        dbond (float): Distance threshold for grouping particles into clusters.
        bounds (tuple): Bounds for the plot (xmin, xmax, ymin, ymax).
        marker_radius (float): Radius of the marker used for the particles.
        mode (str): 'center' for center-to-center distance, 'surface' for surface-to-surface distance.

    Returns:
        result_matrix (list of dicts): Detailed classification results for each particle.
        crystal_summary_matrix (list of dicts): Summary of classified crystal structures.
    """




    N = coordinates.shape[0]  # Number of particles

    # Adjust threshold based on mode
    if mode == 'surface':
        dbond -= 2.21  # Particle diameter

    # Initialize plot
    plt.figure(figsize=(8, 8))
    plt.axis([bounds[0], bounds[1], bounds[0], bounds[1]])
    plt.gca().set_aspect('equal', adjustable='box')

    def find_clusters(coordinates, neighbors_indices, angles, angle_threshold=5.0):
        N = len(coordinates)
        clusters = []
        visited = set()

        def dfs(particle, cluster, bond_angle):
            stack = [particle]
            while stack:
                current = stack.pop()
                if current not in visited:
                    visited.add(current)
                    cluster.append(current)
                    for neighbor in neighbors_indices[current]:
                        if neighbor < len(angles[current]) and current < len(angles[particle]):
                            neighbor_angle = angles[current][neighbors_indices[current].index(neighbor)]
                            if abs(neighbor_angle - bond_angle) <= angle_threshold:
                                stack.append(neighbor)

        for i in range(N):
            if i not in visited:
                for bond_angle in angles[i]:
                    cluster = []
                    dfs(i, cluster, bond_angle)
                    if cluster:
                        clusters.append(cluster)

        return clusters

    clusters = find_clusters(coordinates, neighbors_indices, angles, angle_threshold)



    # Initialize particle colors
    colors = np.full(N, 'b', dtype=str)

    # Classify bonding angles and color particles accordingly
    for i, angle_list in enumerate(angles):
        for bond_angle in angle_list:
            # Color particles based on bond angle
            if 70 < bond_angle < 140:
                colors[i] = 'g'  # Open link configuration
                for neighbor in neighbors_indices[i]:
                    colors[neighbor] = 'g'
            elif 50 < bond_angle < 70:
                colors[i] = 'r'  # Closed link configuration
                for neighbor in neighbors_indices[i]:
                    colors[neighbor] = 'r'
            elif 140 < bond_angle < 180:
                colors[i] = 'y'  # Stretched link configuration
                for neighbor in neighbors_indices[i]:
                    colors[neighbor] = 'y'


    # Plot the particles
    for i in range(N):
        circle = Circle((coordinates[i, 0], coordinates[i, 1]), radius=marker_radius, edgecolor='black', facecolor=colors[i], linewidth=1)
        plt.gca().add_patch(circle)

    plt.title('Crystal Structure Classification')
    plt.xlabel('X Position')
    plt.ylabel('Y Position')
    plt.show()

    # Create result matrix for each particle
    result_matrix = []
    for i in range(N):
        result_matrix.append({
            "index": i,
            "coordinate": coordinates[i],
            "crystal_type": "Unknown",  # Crystal type determination can be enhanced if needed
            "neighbors_in_crystal": [neighbor for neighbor in neighbors_indices[i] if neighbor in clusters],
            "angle": angles[i],
            "nearest_neighbours": neighbors_indices[i],
            "color": colors[i]
        })

    # Create crystal summary matrix for each cluster
    crystal_summary_matrix = []
    for cluster_id, cluster in enumerate(clusters):
        x_coords = [coordinates[i][0] for i in cluster]
        y_coords = [coordinates[i][1] for i in cluster]
        center_coordinate = (sum(x_coords) / len(x_coords), sum(y_coords) / len(y_coords))

        crystal_type = "Unknown"  # Crystal type can be based on angles or predefined conditions

        # Create summary for the cluster
        crystal_summary_matrix.append({
            "cluster_id": cluster_id,
            "crystal_type": crystal_type,
            "center_coordinate": center_coordinate,
            "particle_indexes": cluster,
            "color": colors[cluster[0]]  # Use color of the first particle as the cluster color
        })

    return result_matrix, crystal_summary_matrix

