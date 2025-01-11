import numpy as np
from pprint import pprint
import pandas as pd
import imageio
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from scipy.spatial import KDTree

def dynamic_executioner(coordinates, output_gif_path='crystal_structure.gif', plot_interval=10, fps=2, result_csv_path='result_matrix.csv', summary_csv_path='crystal_summary_matrix.csv'):
    frames = []

    # Parameters in micrometers
    prtclDiameter = 2.21
    dbond = 1.043 * prtclDiameter
    angle_threshold = 5.0
    calculation_mode = 'center'
    bounds = (-55, 55)
    marker_radius = 1

    # Initialize CSV files
    pd.DataFrame().to_csv(result_csv_path, index=False)
    pd.DataFrame().to_csv(summary_csv_path, index=False)

    # Iterate through the time steps
    for timestep, (x, y) in enumerate(coordinates):
        coordinates = np.column_stack((x, y))

        # Find nearest neighbors using KDTree
        tree = KDTree(coordinates)
        neighbors_indices = tree.query(coordinates, k=3, distance_upper_bound=dbond)[1][:, 1:]

        # Calculate angles between neighbors
        angles = angles_between_neighbors(coordinates, neighbors_indices)

        # Classify crystal structure
        result_matrix, crystal_summary_matrix = crystal_classifier(coordinates, neighbors_indices, angles, angle_threshold, dbond, bounds, marker_radius, calculation_mode)

        # Print or process the results for each time step
        print(f"Time step {timestep}:")
        #pprint(result_matrix)
        #pprint(crystal_summary_matrix)

        # Visualize the results every nth time step
        if timestep % plot_interval == 0:
            fig, ax = plt.subplots(figsize=(8, 8))
            ax.set_xlim(bounds)
            ax.set_ylim(bounds)
            ax.set_aspect('equal', adjustable='box')
            for i in range(len(coordinates)):
                circle = Circle((coordinates[i, 0], coordinates[i, 1]), radius=marker_radius, edgecolor='black', facecolor=result_matrix[i]['color'], linewidth=1)
                ax.add_patch(circle)
            plt.title('Crystal Structure Classification')
            plt.xlabel('X Position')
            plt.ylabel('Y Position')

            # Save the current frame
            fig.canvas.draw()
            image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
            image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
            frames.append(image)
            plt.close(fig)

        # Save result_matrix to CSV
        result_df = pd.DataFrame(result_matrix)
        result_df.to_csv(result_csv_path, mode='a', header=not pd.read_csv(result_csv_path).empty, index=False)

        # Save crystal_summary_matrix to CSV
        summary_df = pd.DataFrame(crystal_summary_matrix)
        summary_df.to_csv(summary_csv_path, mode='a', header=not pd.read_csv(summary_csv_path).empty, index=False)

    # Save frames as a GIF
    imageio.mimsave(output_gif_path, frames, fps)

# Example usage
# coordinates = ...  # Your coordinates data
# dynamic_executioner(coordinates)