import pandas as pd
import numpy as np

def feature_engineering(df4):
    df4['price_per_sqft'] = df4['price'] * 100000 / df4['total_sqft']
    df4.location = df4.location.apply(lambda x: x.strip())

    # Handle locations with fewer than 10 entries
    location_stats = df4['location'].value_counts(ascending=False)
    location_stats_less_than_10 = location_stats[location_stats <= 10]
    df4.location = df4.location.apply(lambda x: 'other' if x in location_stats_less_than_10 else x)
    
    df4 = df4[~(df4.total_sqft / df4.bhk < 300)]  # Remove outliers
    return df4
