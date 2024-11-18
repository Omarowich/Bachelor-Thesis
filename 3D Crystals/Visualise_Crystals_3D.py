from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

def visualize_crystals_3D(coordinates, result_matrix):
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

    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')

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

        # Add scatter point for the particle
        existing_labels = [h.get_label() for h in ax.legend_.legendHandles] if ax.get_legend() else []
        ax.scatter(
            coordinate[0], coordinate[1], coordinate[2],
            color=color, s=50
           # label=crystal_type if crystal_type not in existing_labels else ""
        )

        # Draw lines to neighbors that share the same crystal type
        for neighbor_index in neighbors:
            neighbor_type = result_matrix[neighbor_index]['crystal_type']
            if neighbor_type == crystal_type:  # Only connect neighbors of the same type
                neighbor_coord = coordinates[neighbor_index]
                ax.plot(
                    [coordinate[0], neighbor_coord[0]],
                    [coordinate[1], neighbor_coord[1]],
                    [coordinate[2], neighbor_coord[2]],
                    color=color, linewidth=1
                )

    # Add legend and display the plot
    ax.set_xlabel("X-coordinate")
    ax.set_ylabel("Y-coordinate")
    ax.set_zlabel("Z-coordinate")
    ax.set_title("Particle Crystal Structure Visualization")
    #plt.legend(loc="upper right")

    # Enable interactive mode
    plt.ion()  # Interactive mode ON
    plt.show()
    #plt.pause(100)



