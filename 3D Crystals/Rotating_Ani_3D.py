import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.animation as animation

def visualize_rotating_3D(coordinates, result_matrix, save_path="C:\\Users\\omare\\Downloads\\crystal_animation.mp4"):
    # Define colors for crystal types
    crystal_colors = {
        "Hexagonal": "blue",
        "Cubic": "green",
        "Unknown": "gray"
    }

    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Plot particles
    for entry in result_matrix:
        index = entry['index']
        coordinate = entry['coordinate']
        crystal_type = entry['crystal_type']

        color = crystal_colors.get(crystal_type, "black")
        ax.scatter(coordinate[0], coordinate[1], coordinate[2], color=color, s=50)

    # Set labels and title
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title("3D Crystal Visualization")

    # Create the update function for the animation
    def update(num_frame):
        ax.view_init(elev=20., azim=num_frame)  # Update the view to rotate the plot

    # Create the animation object
    ani = animation.FuncAnimation(fig, update, frames=360, interval=50)

    # Save the animation as a video (e.g., .mp4 file)
    ani.save(save_path, writer='ffmpeg', fps=30)

    plt.show()