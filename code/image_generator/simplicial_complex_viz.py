import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import distance_matrix
from itertools import combinations
import networkx as nx

# Create a closed, wavy curve that is not a circle.
# Here we use a perturbed circle with radius varying as r(t) = 1 + 0.3*cos(5t)
n_points = 30
t = np.linspace(0, 2 * np.pi, n_points, endpoint=False)
r_values = 1 + 0.3 * np.cos(5 * t)  # wavy modulation along the circle
x = r_values * np.cos(t)
y = r_values * np.sin(t)
points = np.vstack((x, y)).T

# Set parameters
epsilon = 0.35
tol = 1e-8  # tolerance to overcome floating point inaccuracies

# 1. Plot the raw point cloud
plt.figure(figsize=(4, 4))
plt.scatter(points[:, 0], points[:, 1], color='black')
plt.title("Figure 1: Point Set Data Cloud (Wavy Curve)")
plt.axis('equal')
plt.axis('off')
plt.savefig("figure1_non_circle.png", bbox_inches='tight')
plt.close()

# 2. Plot the point cloud with circles of radius ε around each point
plt.figure(figsize=(4, 4))
plt.scatter(points[:, 0], points[:, 1], color='black')
for (px, py) in points:
    circle = plt.Circle((px, py), epsilon, color='blue', alpha=0.3)
    plt.gca().add_patch(circle)
plt.title("Figure 2: Data Cloud with Radius ε")
plt.axis('equal')
plt.axis('off')
plt.savefig("figure2.png", bbox_inches='tight')
plt.close()

# 3. Build and plot the Vietoris–Rips Complex using the tolerance.
# Compute pairwise distances.
dist_matrix = distance_matrix(points, points)

# Build edges using a tolerance in the distance check.
edges = [(i, j) for i, j in combinations(range(n_points), 2)
         if dist_matrix[i, j] <= epsilon*2 + tol]

# Optionally, compute triangles (2-simplices) for a richer visualization.
triangles = [list(tri) for tri in combinations(range(n_points), 3)
             if (dist_matrix[tri[0], tri[1]] <= epsilon*2 + tol and
                 dist_matrix[tri[1], tri[2]] <= epsilon*2 + tol and
                 dist_matrix[tri[0], tri[2]] <= epsilon*2 + tol)]

# Build a graph for visualization.
G = nx.Graph()
G.add_nodes_from(range(n_points))
G.add_edges_from(edges)

plt.figure(figsize=(4, 4))
pos = {i: (points[i][0], points[i][1]) for i in range(n_points)}
nx.draw(G, pos, node_color='black', node_size=30, edge_color='black', with_labels=False)

#  Fill with color.
for tri in triangles:
    pts = [points[i] for i in tri]
    polygon = plt.Polygon(pts, closed=True, color='brown', alpha=0.5)
    plt.gca().add_patch(polygon)

plt.title("Figure 3: Vietoris–Rips Complex (with tol)")
plt.axis('equal')
plt.axis('off')
plt.savefig("figure3.png", bbox_inches='tight')
plt.close()
