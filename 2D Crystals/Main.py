import numpy as np
from pprint import pprint

from Data_Reader import read_particle_data
from Nearest_Partners import find_nearest_neighbors
from Particle_Angels import angles_between_neighbors
from Classify_Crystals import  classify_crystal_structure
from Visualise_Crystals import visualize_crystals




#coordinates = read_particle_data(r"RandXY1.xlsx")
#coordinates = read_particle_data(r"RandXY2 (triangles try).xlsx")
#coordinates = read_particle_data(r"RandXY3 (many geometrics).xlsx")
coordinates = read_particle_data(r"RandXY4 (a few shapes).xlsx")




# Find nearest neighbors
neighbors_indices = find_nearest_neighbors(coordinates,2,1500)

# Calculate angles between neighbors
angles = angles_between_neighbors(coordinates, neighbors_indices)

# Classify crystal structure
result_matrix, crystal_summary_matrix = classify_crystal_structure(coordinates, neighbors_indices, angles, 10,1500)
pprint(result_matrix)
pprint(crystal_summary_matrix)

# Visualize the results
visualize_crystals(coordinates, result_matrix)