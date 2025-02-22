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




# Parameters
prtclDiameter = 2.21
dbond = 1.043 * prtclDiameter

marker_radius = 1


bounds = (-55, 55)  # Plot bounds

file_path = 'positions.mat'
file_path_v2 = 'positions_v2.mat'
# Load positions
positions = loadmat(file_path)['positions']
positions_v2 = loadmat(file_path_v2)['positions']



# Perform analyses
#angle_distance = particle_angle_analysis_distance(positions, dbond, bounds,marker_radius,'center', prtclDiameter)
#angle_v2 = particle_angle_analysis_v2(positions_v2, dbond, bounds,marker_radius, 'center', prtclDiameter)




# extra Analysis
cluster_hc = particle_cluster_analysis_hc(positions, dbond, bounds, marker_radius)
cluster_distance = particle_cluster_analysis_distance(positions, dbond, bounds, marker_radius)
angle_hc = particle_angle_analysis_hc(positions, dbond, bounds, marker_radius)
radius_of_gyration_hc = particle_radius_of_gyration_analysis_hc(positions, dbond, bounds, marker_radius)