import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def visualize_Surface_Plot_3D(coordinates, result_matrix):
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

    # Create a grid for the surface plot
    x = np.linspace(0, 3, 100)
    y = np.linspace(0, 3, 100)
    X, Y = np.meshgrid(x, y)
    Z = np.zeros_like(X)

    # Fill Z with the appropriate values based on coordinates
    for entry in result_matrix:
        coordinate = entry['coordinate']
        Z += np.exp(-((X - coordinate[0])**2 + (Y - coordinate[1])**2) / 0.1)

    # Plot the surface
    ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none')

    # Add labels and title
    ax.set_xlabel("X-coordinate")
    ax.set_ylabel("Y-coordinate")
    ax.set_zlabel("Z-coordinate")
    ax.set_title("Particle Crystal Structure Visualization")

    # Enable interactive mode
    plt.ion()  # Interactive mode ON
    plt.show()