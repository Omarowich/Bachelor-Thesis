import numpy as np
import math

def angles_between_neighbors(coordinates, neighbors_indices):
    """
    Calculate bond angles between each particle and its two nearest neighbors.

    Parameters:
    coordinates (list of lists): The list of particle coordinates, [[x1, y1], [x2, y2], ...].
    neighbors_indices (list of lists): The indices of the nearest neighbors for each particle.

    Returns:
    list of lists: Each inner list contains the bond angles (in degrees) for each particle.
    """
    all_angles = []

    for i, neighbors in enumerate(neighbors_indices):
        if len(neighbors) < 2:
            all_angles.append([])  # Not enough neighbors to form an angle
            continue

        p1 = np.array(coordinates[i])
        n1 = np.array(coordinates[neighbors[0]])
        n2 = np.array(coordinates[neighbors[1]])

        # Vectors from the central particle to each neighbor
        v1 = n1 - p1
        v2 = n2 - p1

        # Calculate the angle between the vectors
        cos_theta = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        angle = math.degrees(np.arccos(np.clip(cos_theta, -1.0, 1.0)))

        all_angles.append([angle])

    return all_angles