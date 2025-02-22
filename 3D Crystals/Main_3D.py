import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint

from Data_Reader_3D import read_particle_data_3D
from Nearest_Partners_3D import find_nearest_neighbors_3D
from Particle_Angels_3D import angles_between_neighbors_3D
from Classify_Crystals_3D import  classify_crystal_structure_3D
from Visualise_Crystals_3D import visualize_crystals_3D
from Rotating_Ani_3D import visualize_rotating_3D
from Visualize_SurfacePlot_3D import visualize_Surface_Plot_3Dx




coordinates = read_particle_data_3D(r"RandXYZ(Cube).xlsx")
#coordinates = read_particle_data_3D(r"RandXYZ( 10 Really Random now).xlsx")
#coordinates = read_particle_data_3D(r"RandXYZ more( 100 Really Random now).xlsx")

#  Does not handle 2D data
#coordinates = read_particle_data_3D(r"C:\Users\omare\PycharmProjects\Crytal Detector BA Trial\2D Crystals\RandXY3 (many geometrics).xlsx")



# Find nearest neighbors
neighbors_indices = find_nearest_neighbors_3D(coordinates,3,50)

# Calculate angles between neighbors
angles = angles_between_neighbors_3D(coordinates, neighbors_indices,2)

# Classify crystal structure
result_matrix, crystal_summary_matrix = classify_crystal_structure_3D(coordinates, neighbors_indices, angles, 100,50)
pprint(result_matrix)
pprint(crystal_summary_matrix)

# Visualize the results
visualize_crystals_3D(coordinates, result_matrix)
#visualize_Surface_Plot_3D(coordinates, result_matrix)


# Visualize the results in a Rotation Animation

#just remove the Hashtag "#" from the next line to see the animation
#visualize_rotating_3D(coordinates, result_matrix)

"""
ax = plt.axes(projection='3d')

xd=np.arange(-5,5,0.1)
yd=np.arange(-5,5,0.1)

X,Y = np.meshgrid(xd,yd)
Z = np.cos(X)*np.sin(Y)

ax.plot_surface(X,Y,Z,cmap='viridis')
plt.show()

"""