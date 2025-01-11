import numpy as np
from pprint import pprint
import pandas as pd

from Data_Reader import read_particle_data
from Nearest_Partners import find_nearest_neighbors
from Particle_Angels import angles_between_neighbors
from Classify_Crystals import  classify_crystal_structure
from New_Crystal_Classificator import crystal_classifier
from Visualise_Crystals import visualize_crystals
from Mat_Data_Reader import Mat_read_particle_data
from data_reader_csv import read_particle_data_csv
from dynamic_executioner import dynamic_executioner






coordinates = Mat_read_particle_data(r"C:\Users\omare\PycharmProjects\Crytal Detector BA Trial\Matlab Crystal Thing\positions.mat")
#coordinates = Mat_read_particle_data(r"C:\Users\omare\PycharmProjects\Crytal Detector BA Trial\Matlab Crystal Thing\positions_v2.mat")




# Parameters in micrometers
prtclDiameter = 2.21
dbond = 1.043 * prtclDiameter

angle_threshold = 5.0
calculation_mode = 'center'

bounds = (-55, 55)
marker_radius = 1





# Find nearest neighbors
neighbors_indices = find_nearest_neighbors(coordinates,2,dbond)

# Calculate angles between neighbors
angles = angles_between_neighbors(coordinates, neighbors_indices)

# Classify crystal structure
#result_matrix, crystal_summary_matrix = classify_crystal_structure(coordinates, neighbors_indices, angles, 10,dbond)
result_matrix, crystal_summary_matrix = crystal_classifier(coordinates, neighbors_indices, angles, angle_threshold, dbond, bounds, marker_radius, calculation_mode)
pprint(result_matrix)
pprint(crystal_summary_matrix)

# Visualize the results
#visualize_crystals(coordinates, result_matrix)