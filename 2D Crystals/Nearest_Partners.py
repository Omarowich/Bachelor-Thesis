import numpy as np


def find_nearest_neighbors(coordinates, n_neighbors, max_distance=15.0):
    num_particles = len(coordinates)
    nearest_neighbors = []

    for i in range(num_particles):
        distances = []

        # Compute distance from particle i to all other particles
        for j in range(num_particles):
            if i != j:
                dist = np.linalg.norm(np.array(coordinates[i]) - np.array(coordinates[j]))
                # Include only neighbors within max_distance
                if dist <= max_distance:
                    distances.append((dist, j))

        # Sort distances and get indices of the n nearest neighbors
        distances.sort(key=lambda x: x[0])
        nearest_indices = [index for _, index in distances[:n_neighbors]]

        # Append the nearest neighbors for particle i
        nearest_neighbors.append(nearest_indices)

    return nearest_neighbors






def find_nearest_neighbors_for_particle(coordinates, particle_index, n_neighbors):
    num_particles = len(coordinates)
    distances = []

    # Compute distances from the specified particle to all other particles
    for j in range(num_particles):
        if particle_index != j:
            dist = np.linalg.norm(np.array(coordinates[particle_index]) - np.array(coordinates[j]))
            distances.append((dist, j))  # store distance and index of the neighbor

    # Sort distances and get indices of the three nearest neighbors
    distances.sort(key=lambda x: x[0])
    nearest_indices = [index for _, index in distances[:n_neighbors]]

    return nearest_indices