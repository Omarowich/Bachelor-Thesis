import numpy as np
import math
from itertools import combinations


def angles_between_neighbors(coordinates, neighbors_indices):
    """
    Calculate acute angles between each particle's nearest neighbors (angles between triplets of particles).

    Parameters:
    coordinates (list of lists): The list of particle coordinates, [[x1, y1], [x2, y2], ...].
    neighbors_indices (list of lists): The indices of the nearest neighbors for each particle.

    Returns:
    list of lists: Each inner list contains the acute angles (in degrees) between each triplet of neighbors
                   for each particle.
    """
    all_angles = []

    for i, neighbors in enumerate(neighbors_indices):
        particle_angles = []
        p1 = np.array(coordinates[i])

        # Calculate angles between each unique triplet (p1 and two neighbors)
        for n1, n2 in combinations(neighbors, 2):
            # Vectors from the central particle to each neighbor
            v1 = np.array(coordinates[n1]) - p1
            v2 = np.array(coordinates[n2]) - p1

            # Calculate the angle between the vectors
            cos_theta = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
            angle = math.degrees(np.arccos(np.clip(cos_theta, -1.0, 1.0)))

            # Ensure the angle is acute (<= 90 degrees)
            if angle > 90:
                angle = 180 - angle

            particle_angles.append(angle)

        # Store the angles for this particle
        all_angles.append(particle_angles)

    return all_angles
