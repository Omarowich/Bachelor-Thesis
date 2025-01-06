import numpy as np

def classify_crystal_structure(coordinates, neighbors_indices, all_angles, angle_threshold=5.0, distance_threshold=20.0):
    angle_clusters = []
    result_matrix = []
    crystal_summary_matrix = []

    def is_closed_shape(cluster):
        for particle in cluster:
            neighbors_in_cluster = [neighbor for neighbor in neighbors_indices[particle] if neighbor in cluster]
            if len(neighbors_in_cluster) < 2:
                return False
        return True

    def is_all_connected(cluster):
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

    def assign_crystal_type(cluster, angles):
        for angle in angles:
            if 70 < angle < 140:
                return "Open Link Configuration", 'g'
            elif 50 < angle < 70:
                return "Closed Link Configuration", 'r'
        return "Unknown", 'b'

    def merge_clusters(angle_clusters):
        merged = []
        processed = set()
        for i, cluster in enumerate(angle_clusters):
            if i in processed:
                continue
            current_merge = set(cluster)
            for j, other in enumerate(angle_clusters):
                if i != j and any(p in current_merge for p in other):
                    current_merge.update(other)
                    processed.add(j)
            merged.append(list(current_merge))
        return merged

    for i, angles in enumerate(all_angles):
        added_to_cluster = False
        for cluster in angle_clusters:
            cluster_representative = cluster[0]
            representative_angles = all_angles[cluster_representative]
            if all(abs(a - b) <= angle_threshold for a, b in zip(angles, representative_angles)):
                temp_cluster = cluster + [i]
                if is_all_connected(temp_cluster):
                    cluster.append(i)
                    added_to_cluster = True
                    break
        if not added_to_cluster:
            angle_clusters.append([i])

    angle_clusters = merge_clusters(angle_clusters)

    for i in range(len(coordinates)):
        particle_cluster = next((cluster for cluster in angle_clusters if i in cluster), None)
        cluster_id = angle_clusters.index(particle_cluster) if particle_cluster else None

        if particle_cluster and is_closed_shape(particle_cluster):
            crystal_type, color = assign_crystal_type(particle_cluster, all_angles[particle_cluster[0]])
            neighbors_in_crystal = [neighbor for neighbor in neighbors_indices[i] if neighbor in particle_cluster]
        else:
            crystal_type, color = "Unknown", 'b'
            neighbors_in_crystal = []

        result_matrix.append({
            "index": i,
            "coordinate": coordinates[i],
            "crystal_type": crystal_type,
            "neighbors_in_crystal": neighbors_in_crystal,
            "angle": all_angles[i],
            "nearest_neighbours": neighbors_indices[i],
            "cluster_id": cluster_id,
            "color": color
        })

    for cluster_id, cluster in enumerate(angle_clusters):
        if is_closed_shape(cluster):
            crystal_type, color = assign_crystal_type(cluster, all_angles[cluster[0]])
            x_coords = [coordinates[i][0] for i in cluster]
            y_coords = [coordinates[i][1] for i in cluster]
            center_coordinate = (sum(x_coords) / len(x_coords), sum(y_coords) / len(y_coords))
            crystal_summary_matrix.append({
                "cluster_id": cluster_id,
                "crystal_type": crystal_type,
                "center_coordinate": center_coordinate,
                "particle_indexes": cluster,
                "color": color
            })

    return result_matrix, crystal_summary_matrix