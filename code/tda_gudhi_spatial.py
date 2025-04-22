# tda_spatial_gudhi.py
import gudhi
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
matplotlib.rcParams['text.usetex'] = False


# Load and preprocess data
df = pd.read_csv('Skyserver_SQL3_16_2025 8_52_53 PM.csv', dtype=str)
df.columns = df.columns.str.strip()
df = df.apply(pd.to_numeric, errors='coerce')
df.dropna(subset=['ra', 'dec', 'redshift'], inplace=True)
df = df.sample(frac=1).reset_index(drop=True)

# Spatial point cloud
points = df[['ra', 'dec', 'redshift']].values[:1000]

# Create Rips complex
rips_complex = gudhi.RipsComplex(points=points, max_edge_length=5.0)
simplex_tree = rips_complex.create_simplex_tree(max_dimension=2)

# Print summary
print(f"Rips complex dimension: {simplex_tree.dimension()}")
print(f"Number of simplices: {simplex_tree.num_simplices()}")
print(f"Number of vertices: {simplex_tree.num_vertices()}")

# Compute persistence
simplex_tree.compute_persistence()

# Persistence diagram
gudhi.plot_persistence_diagram(simplex_tree.persistence())
plt.title('Spatial Persistence Diagram (RA, DEC, Redshift)')
plt.savefig('persistence_diagram.png')
plt.show()

# Persistence barcode
gudhi.plot_persistence_barcode(simplex_tree.persistence())
plt.title('Spatial Persistence Barcode (RA, DEC, Redshift)')
plt.savefig('persistence_barcode.png')
plt.show()

# Nice 3D visualization of the spatial point cloud
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(df['ra'], df['dec'], df['redshift'], s=5, alpha=0.5, c=df['redshift'], cmap='viridis')

ax.set_xlabel('Right Ascension (RA)')
ax.set_ylabel('Declination (DEC)')
ax.set_zlabel('Redshift (Distance)')
ax.set_title('3D Spatial Distribution of Galaxies')

plt.tight_layout()
plt.savefig('3D_Spatial_Distribution.png')
plt.show()
