import pandas as pd


def read_particle_data_3D(file_path, sheet_name=0):
    # Load the Excel file
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    df = df.dropna(subset=['x', 'y', 'z'])
    # Read columns named 'x' and 'y' for coordinates
    x_coords = df['x'].tolist()
    y_coords = df['y'].tolist()
    z_coords = df['z'].tolist()

    coordinates = list(zip(x_coords, y_coords, z_coords))

    return coordinates
