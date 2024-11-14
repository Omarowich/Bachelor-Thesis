import matplotlib.pyplot as plt
import numpy as np


def visualize_crystals(coordinates, result_matrix):
    """
    Visualize particles with colors based on crystal types and lines connecting neighbors.

    Parameters:
    coordinates (list of lists): The list of particle coordinates, [[x1, y1], [x2, y2], ...].
    result_matrix (list of dicts): Contains information about each particle, including
                                   'index', 'coordinate', 'crystal_type', and 'neighbors_in_crystal'.
    """
    # Define colors for crystal types
    crystal_colors = {
        "Hexagonal": "blue",
        "Cubic": "green",
        "Unknown": "gray"
    }



    # Create a unique color for each crystal type
    unique_crystal_types = set(entry['crystal_type'] for entry in result_matrix)
    colors = plt.cm.get_cmap("Set1", len(unique_crystal_types))  # Use a colormap for unique colors
    crystal_colors = {crystal_type: colors(i) for i, crystal_type in enumerate(unique_crystal_types)}

    plt.figure(figsize=(8, 8))

    # Plot particles and connections
    for entry in result_matrix:
        index = entry['index']
        coordinate = entry['coordinate']
        crystal_type = entry['crystal_type']
        neighbors = entry['neighbors_in_crystal']

        # Get the color based on crystal type
        color = crystal_colors.get(crystal_type, "black")  # Default to black if type is unknown


        # Set color to black for unknown or single-particle types
        if crystal_type == "Unknown" or len(neighbors) == 0:
            color = "black"
        else:
            # Get the color based on crystal type
            color = crystal_colors.get(crystal_type, "black")  # Default to black if type is unknown

        plt.scatter(coordinate[0], coordinate[1], color=color, s=50,
                    label=crystal_type if color not in plt.gca().get_legend_handles_labels()[1] else "")

        # Draw lines to neighbors that share the same crystal type
        for neighbor_index in neighbors:
            neighbor_type = result_matrix[neighbor_index]['crystal_type']
            if neighbor_type == crystal_type:  # Only connect neighbors of the same type
                neighbor_coord = coordinates[neighbor_index]
                plt.plot([coordinate[0], neighbor_coord[0]], [coordinate[1], neighbor_coord[1]], color=color,
                         linewidth=1)



    # Add legend and display the plot
    plt.xlabel("X-coordinate")
    plt.ylabel("Y-coordinate")
    plt.title("Particle Crystal Structure Visualization")
   # plt.legend(loc="upper right")
    plt.axis("equal")
    plt.show()




