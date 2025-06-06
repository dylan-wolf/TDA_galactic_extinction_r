# tda_multiparameter_rivet.py
import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist, squareform

# Load and preprocess data
df = pd.read_csv('Skyserver_SQL3_16_2025 8_52_53 PM.csv', dtype=str)
df.columns = df.columns.str.strip()
df = df.apply(pd.to_numeric, errors='coerce')
df.dropna(subset=['ra', 'dec', 'redshift', 'extinction_r'], inplace=True)
df = df.sample(n=10000, random_state=42).reset_index(drop=True)
# df = df.sample(frac=1).reset_index(drop=True)

# Extract spatial points and extinction values
spatial_points = df[['ra', 'dec', 'redshift']].values
extinction_values = df['extinction_r'].values

# Compute pairwise spatial distances
spatial_dist_matrix = squareform(pdist(spatial_points))

# Create a RIVET-compatible bifiltration file
num_points = len(df)
with open('rivet_input.txt', 'w') as f:
    f.write('--datatype points\n')
    f.write(f"{num_points} {num_points}\n")
    for i in range(num_points):
        # Use extinction value and the distance to the nearest neighbor (excluding self, which is zero)
        nearest_neighbor_dist = np.sort(spatial_dist_matrix[i])[1]
        f.write(f"{extinction_values[i]}, {nearest_neighbor_dist}\n")

print("RIVET input file 'rivet_input.txt' created.")
