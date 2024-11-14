import numpy as np

def classify_crystal_structure(coordinates, neighbors_indices, all_angles, angle_threshold=5.0, distance_threshold=20.0):
    angle_clusters = []
    result_matrix = []
    crystal_summary_matrix = []

    # Function to validate that the cluster forms a closed shape
    def is_closed_shape(cluster):
        for particle in cluster:
            neighbors_in_cluster = [
                neighbor for neighbor in neighbors_indices[particle] if neighbor in cluster
            ]
            if len(neighbors_in_cluster) < 2:
                return False
        return True

    def is_all_connected(cluster):
        """Ensure all particles in a cluster are connected."""
        visited = set()

        def dfs(particle):
            if particle in visited:
                return
            visited.add(particle)
            for neighbor in neighbors_indices[particle]:
                if neighbor in cluster:
                    dfs(neighbor)

        dfs(cluster[0])
        return len(visited) == len(cluster)

    def assign_crystal_type(cluster):
        if len(cluster) == 6:
            return "Hexagonal"
        elif len(cluster) == 4:
            return "Cubic"
        elif len(cluster) == 3:
            return "Triangular"
        elif len(cluster) == 5:
            return "Pentagonal"
        elif len(cluster) == 7:
            return "Septagonal"
        elif len(cluster) == 8:
            return "Octagonal"
        else:
            return "Unknown"

    # Identify and add potential shapes to angle_clusters
    for i, angles in enumerate(all_angles):
        added_to_cluster = False

        for cluster in angle_clusters:
            cluster_representative = cluster[0]
            representative_angles = all_angles[cluster_representative]

            # Check if the angles match within the threshold
            if all(abs(a - b) <= angle_threshold for a, b in zip(angles, representative_angles)):
                temp_cluster = cluster + [i]
                if is_all_connected(temp_cluster):
                    cluster.append(i)
                    added_to_cluster = True
                    break

        # If not added to any cluster, create a new cluster
        if not added_to_cluster:
            angle_clusters.append([i])

    for i in range(len(coordinates)):
        particle_cluster = next((cluster for cluster in angle_clusters if i in cluster), None)
        cluster_id = angle_clusters.index(particle_cluster) if particle_cluster else None

        if particle_cluster and is_closed_shape(particle_cluster):
            crystal_type = assign_crystal_type(particle_cluster)
            neighbors_in_crystal = [
                neighbor for neighbor in neighbors_indices[i] if neighbor in particle_cluster
            ]
        else:
            crystal_type = "Unknown"
            neighbors_in_crystal = []

        result_matrix.append({
            "index": i,
            "coordinate": coordinates[i],
            "crystal_type": crystal_type,
            "neighbors_in_crystal": neighbors_in_crystal,
            "angle": all_angles[i],
            "nearest_neighbours": neighbors_indices[i],
            "cluster_id": cluster_id
        })

    for cluster_id, cluster in enumerate(angle_clusters):
        if is_closed_shape(cluster):
            crystal_type = assign_crystal_type(cluster)

            x_coords = [coordinates[i][0] for i in cluster]
            y_coords = [coordinates[i][1] for i in cluster]
            center_coordinate = (sum(x_coords) / len(x_coords), sum(y_coords) / len(y_coords))

            crystal_summary_matrix.append({
                "cluster_id": cluster_id,
                "crystal_type": crystal_type,
                "center_coordinate": center_coordinate,
                "particle_indexes": cluster
            })

    return result_matrix, crystal_summary_matrix







"""
    def filter_nearest_neighbors(particle, neighbors, max_distance=15.0):
       #Filter neighbors based on a stricter distance threshold to avoid lone particles.
        particle_coord = coordinates[particle]
        valid_neighbors = []
        for neighbor in neighbors:
            neighbor_coord = coordinates[neighbor]
            distance = np.linalg.norm(np.array(particle_coord) - np.array(neighbor_coord))
            if distance <= max_distance:
                valid_neighbors.append(neighbor)
        return valid_neighbors

    def identify_potential_shapes():
        potential_shapes = []
        for i, angles in enumerate(all_angles):
            added_to_shape = False
            valid_neighbors = filter_nearest_neighbors(i, neighbors_indices[i])

            for shape in potential_shapes:
                representative = shape[0]
                rep_angles = all_angles[representative]

                # Check angle similarity within threshold
                if all(abs(a - b) <= angle_threshold for a, b in zip(angles, rep_angles)):
                    temp_shape = shape + [i]
                    if is_all_connected(temp_shape) and len(temp_shape) > 2:
                        shape.append(i)
                        added_to_shape = True
                        break

            if not added_to_shape and len(valid_neighbors) >= 2:
                potential_shapes.append([i])

        filtered_shapes = [shape for shape in potential_shapes if is_closed_shape(shape)]
        return filtered_shapes
"""




"""
  potential_shapes = identify_potential_shapes()

  for shape in potential_shapes:
      if is_closed_shape(shape):
          angle_clusters.append(shape)
          
          ##
          #
        
  """


