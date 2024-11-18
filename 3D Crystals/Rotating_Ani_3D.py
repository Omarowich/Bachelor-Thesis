import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter, FFMpegWriter
from mpl_toolkits.mplot3d import Axes3D
import webbrowser
import os
import subprocess

def visualize_rotating_3D(coordinates, result_matrix):


    coordinates = np.array(coordinates)

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

    # Initialize the figure and 3D axis
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Get the min and max values for each axis to properly scale the plot
    x_min, x_max = np.min(coordinates[:, 0]), np.max(coordinates[:, 0])
    y_min, y_max = np.min(coordinates[:, 1]), np.max(coordinates[:, 1])
    z_min, z_max = np.min(coordinates[:, 2]), np.max(coordinates[:, 2])

    # Add a padding around the data points for better visualization
    padding = 0.1
    ax.set_xlim(x_min - padding, x_max + padding)
    ax.set_ylim(y_min - padding, y_max + padding)
    ax.set_zlim(z_min - padding, z_max + padding)

    # Plot particles and connections
    def update(frame):
        ax.cla()  # Clear the axes to redraw the plot

        # Plot particles again with updated data
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
                color = crystal_colors.get(crystal_type, "black")  # Default to black if type is unknown

            ax.scatter(coordinate[0], coordinate[1], coordinate[2], color=color, s=50)

            # Draw lines to neighbors that share the same crystal type
            for neighbor_index in neighbors:
                neighbor_type = result_matrix[neighbor_index]['crystal_type']
                if neighbor_type == crystal_type:  # Only connect neighbors of the same type
                    neighbor_coord = coordinates[neighbor_index]
                    ax.plot([coordinate[0], neighbor_coord[0]], [coordinate[1], neighbor_coord[1]], [coordinate[2], neighbor_coord[2]], color=color, linewidth=1)

        # Rotate the view slightly at each frame
        ax.view_init(azim=frame)

        return []

    # Create the animation
    ani = FuncAnimation(fig, update, frames=np.arange(0, 360, 2), interval=100, blit=False)

    # Save the animation as an MP4 file using FFMpegWriter
    save_path = r'C:\Users\omare\Downloads\rotating_crystal_animation.mp4'
    writer = FFMpegWriter(fps=30, metadata=dict(artist='Me'), bitrate=1800)
    ani.save(save_path, writer=writer)

    # Open the saved animation
    if os.name == 'nt':  # Windows
        os.startfile(save_path)  # This will open the file in its default associated application (e.g., browser)
        subprocess.run(['start', save_path], shell=True)
    else:
        webbrowser.open('file://' + save_path)  # Open in default browser
