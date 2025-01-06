import numpy as np


def find_nearest_neighbors(coordinates, n_neighbors, dbond):
    num_particles = len(coordinates)
    nearest_partners = []

    for i in range(num_particles):
        distances = []

        # Compute distances from particle i to all other particles
        for j in range(num_particles):
            if i != j:
                dist = np.linalg.norm(np.array(coordinates[i]) - np.array(coordinates[j]))
                # Include only neighbors within dbond
                if dist <= dbond:
                    distances.append((dist, j))

        # Sort distances and get indices of the two nearest neighbors
        distances.sort(key=lambda x: x[0])
        nearest_indices = [index for _, index in distances[:2]]

        # Append the two nearest partners for particle i
        nearest_partners.append(nearest_indices)

    return nearest_partners

