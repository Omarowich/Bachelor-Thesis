import scipy.io
import numpy as np

def Mat_read_particle_data(file_path):
    """
    Read particle data from a .mat file.

    Parameters:
        file_path (str): Path to the .mat file.

    Returns:
        numpy.ndarray: Array of particle positions.
    """
    mat = scipy.io.loadmat(file_path)
    # Assuming the positions are stored under the key 'positions'
    positions = mat['positions']
    return positions