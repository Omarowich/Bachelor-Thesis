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




#coordinates = read_particle_data(r"RandXY1.xlsx")
#coordinates = read_particle_data(r"RandXY2 (triangles try).xlsx")
#coordinates = read_particle_data(r"RandXY3 (many geometrics).xlsx")
#coordinates = read_particle_data(r"RandXY4 (a few shapes).xlsx")


#coordinates = Mat_read_particle_data(r"C:\Users\omare\PycharmProjects\Crytal Detector BA Trial\Matlab Crystal Thing\positions.mat")
#coordinates = Mat_read_particle_data(r"C:\Users\omare\PycharmProjects\Crytal Detector BA Trial\Matlab Crystal Thing\positions_v2.mat")



#Dynamic Coordinates

coordDynX = read_particle_data_csv(r"C:\Users\omare\PycharmProjects\Crytal Detector BA Trial\Matlab Crystal Thing\position_x.csv")
coordDynY = read_particle_data_csv(r"C:\Users\omare\PycharmProjects\Crytal Detector BA Trial\Matlab Crystal Thing\position_y.csv")

coordDynXY = zip(coordDynX, coordDynY)  # zip the two lists together





# Parameters in micrometers
prtclDiameter = 2.21
dbond = 1.043 * prtclDiameter

angle_threshold = 5.0
calculation_mode = 'center'

bounds = (-55, 55)
marker_radius = 1



output_gif_path = 'crystal_structure.gif'
result_csv_path='result_matrix.csv'
summary_csv_path='crystal_summary_matrix.csv'

dynamic_executioner(coordDynXY, output_gif_path, 10,2,result_csv_path,summary_csv_path)


"""
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

"""