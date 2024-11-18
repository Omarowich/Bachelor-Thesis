import numpy as np


def classify_crystal_structure_3D(coordinates, neighbors_indices, all_angles, angle_threshold=5.0,
                               distance_threshold=20.0):
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

    def assign_crystal_type_3D(cluster, all_angles, angle_threshold=5.0):
        angles = [all_angles[particle] for particle in cluster]
        flattened_angles = [angle for sublist in angles for angle in sublist]

        if len(cluster) == 6 and all(abs(angle - 90) <= angle_threshold for angle in flattened_angles):
            return "Hexagonal"
        elif len(cluster) == 8 and all(abs(angle - 90) <= angle_threshold for angle in flattened_angles):
            return "Cubic"
        elif len(cluster) == 4 and all(abs(angle - 60) <= angle_threshold for angle in flattened_angles):
            return "Tetrahedral"
        elif len(cluster) == 12 and all(abs(angle - 60) <= angle_threshold for angle in flattened_angles):
            return "Icosahedral"
        elif len(cluster) == 20 and all(abs(angle - 60) <= angle_threshold for angle in flattened_angles):
            return "Dodecahedral"
        else:
            return "Unknown"

    def merge_clusters(angle_clusters):
        """
        Merge clusters that share particles, allowing particles to belong to multiple clusters.

        Parameters:
        angle_clusters (list of lists): The initial list of clusters.

        Returns:
        list of lists: The updated list of merged clusters, including overlaps.
        """
        merged = []  # Final list of merged clusters
        processed = set()  # Tracks clusters we've already processed

        for i, cluster in enumerate(angle_clusters):
            # Skip clusters we've already processed
            if i in processed:
                continue

            # Start a new merged cluster
            current_merge = set(cluster)

            # Check for overlaps with other clusters
            for j, other in enumerate(angle_clusters):
                if i != j and any(p in current_merge for p in other):
                    # Overlap found: include `other` in the current merge
                    current_merge.update(other)
                    processed.add(j)  # Mark this cluster as processed

            # Add the merged cluster
            merged.append(list(current_merge))

        return merged

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

    # Merge clusters to ensure connected particles form single clusters
    angle_clusters = merge_clusters(angle_clusters)

    for i in range(len(coordinates)):
        particle_cluster = next((cluster for cluster in angle_clusters if i in cluster), None)
        cluster_id = angle_clusters.index(particle_cluster) if particle_cluster else None

        if particle_cluster and is_closed_shape(particle_cluster):
            crystal_type = assign_crystal_type_3D(particle_cluster, all_angles, angle_threshold)
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
            crystal_type = assign_crystal_type_3D(cluster, all_angles, angle_threshold)

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