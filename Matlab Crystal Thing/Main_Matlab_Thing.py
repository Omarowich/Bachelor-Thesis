import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform
from matplotlib.patches import Rectangle




file_path = 'positions_v2.npy'  # Update with your file's path
threshold = 3  # Distance threshold for grouping

# Step 1: Load positions
positions = load_positions(file_path)

# Step 2: Find groups of particles
groups = find_groups(positions, threshold)

# Step 3: Calculate colors based on bonding angles
colors = calculate_colors(positions, groups)

# Step 4: Visualize particles
visualize_particles(positions, colors)