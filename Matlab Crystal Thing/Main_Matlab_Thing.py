import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform
from matplotlib.patches import Rectangle
from scipy.io import loadmat

from particle_cluster_analysis_hc import particle_cluster_analysis_hc
from particle_cluster_analysis_distance import particle_cluster_analysis_distance
from particle_angle_analysis_distance import particle_angle_analysis_distance
from particle_angle_analysis_v2 import particle_angle_analysis_v2
from particle_angle_analysis_hc import particle_angle_analysis_hc
from particle_radius_of_gyration_analysis_hc import particle_radius_of_gyration_analysis_hc



file_path = 'positions.mat'
file_path_v2 = 'positions_v2.mat'
threshold = 3  # Distance threshold for grouping
bounds = (-55, 55)  # Plot bounds

# Load positions
positions = loadmat(file_path)['positions']
positions_v2 = loadmat(file_path_v2)['positions']



# Perform analyses
cluster_hc = particle_cluster_analysis_hc(positions, threshold, bounds)
cluster_distance = particle_cluster_analysis_distance(positions, threshold, bounds)
angle_distance = particle_angle_analysis_distance(positions, threshold, bounds)
angle_v2 = particle_angle_analysis_v2(positions_v2, threshold, bounds)
angle_hc = particle_angle_analysis_hc(positions, threshold, bounds)
radius_of_gyration_hc = particle_radius_of_gyration_analysis_hc(positions, threshold, bounds)