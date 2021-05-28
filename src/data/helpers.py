import pandas as pd
import os

def load(file_name):
    file_path = os.path.join('../../data/external/',file_name)
    data = pd.read_csv(file_path, index_col=0)
    return data