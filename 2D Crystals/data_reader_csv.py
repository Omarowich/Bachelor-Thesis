import numpy as np
from pprint import pprint
import pandas as pd

def read_particle_data_csv(file_path, sheet_name=None):
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
    return df.values
