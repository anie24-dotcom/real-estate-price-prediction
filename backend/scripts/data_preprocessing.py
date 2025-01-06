import pandas as pd
import numpy as np
import matplotlib
from matplotlib import pyplot as plt

# Configure plot size
matplotlib.rcParams["figure.figsize"] = (20, 10)

def load_and_clean_data():
    # Load dataset
    df1 = pd.read_csv("backend/data/Bengaluru_House_Data.csv")
    # Clean the data
    df2 = df1.drop(['area_type','society','balcony','availability'], axis='columns')
    df3 = df2.dropna()
    df3['bhk'] = df3['size'].apply(lambda x: int(x.split(' ')[0]))
    # Handle total_sqft values
    def is_float(x):
        try:
            float(x)
        except:
            return False
        return True
    df3[~df3['total_sqft'].apply(is_float)]

    def convert_sqft_to_num(x):
        tokens = x.split('-')
        if len(tokens) == 2:
            return (float(tokens[0]) + float(tokens[1])) / 2
        try:
            return float(x)
        except:
            return None
    df4 = df3.copy()
    df4.total_sqft = df4.total_sqft.apply(convert_sqft_to_num)
    df4 = df4[df4.total_sqft.notnull()]
    return df4
