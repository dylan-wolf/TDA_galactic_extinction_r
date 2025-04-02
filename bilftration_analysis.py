import pandas as pd
import numpy as np
import gudhi as gd
import matplotlib.pyplot as plt

# --------------------------
# Step 1: Load CSV (spatial data)
# --------------------------
df = pd.read_csv('Skyserver_SQL3_16_2025 8_52_53 PM.csv', dtype=str)
df.columns = df.columns.str.strip()
df = df.apply(pd.to_numeric, errors='coerce')
df.dropna(subset=['ra', 'dec', 'redshift', 'extinction_r'], inplace=True)
df = df.sample(n=10000, random_state=42).reset_index(drop=True)

# Extract spatial coordinates (for Rips complex)
spatial_points = df[['ra', 'dec', 'redshift']].values

# --------------------------
# Step 2: Load precomputed filtration values from rivet_input.txt
# --------------------------
rivet_file = 'rivet_input.txt'
with open(rivet_file, 'r') as f:
    lines = f.readlines()

# Basic checks on rivet file
if len(lines) < 3:
    raise ValueError("Unexpected format in rivet_input.txt.")

# Second line typically: "N M"
n_points_line = lines[1].strip()
n_points = int(n_points_line.split()[0])  # not always needed, but let's parse it

# Read the lines with extinction and nearest-neighbor data
filtration_data = []
for line in lines[2:]:
    parts = line.strip().split(',')
    if len(parts) >= 2:
        try:
            ext_val = float(parts[0].strip())
            nn_val = float(parts[1].strip())
            filtration_data.append((ext_val, nn_val))
        except Exception as e:
            print(f"Error parsing line: {line}\n{e}")

filtration_data = np.array(filtration_data)  # shape (n_points, 2)
if filtration_data.shape[0] != len(spatial_points):
    raise ValueError("Mismatch between number of points in CSV and rivet file.")

extinction_vals = filtration_data[:, 0]
nn_vals = filtration_data[:, 1]

# --------------------------
# Step 3: Define parameter grid
# --------------------------
ext_min, ext_max = np.min(extinction_vals), np.max(extinction_vals)
num_ext = 10
ext_thresholds = np.linspace(ext_min, ext_max, num_ext)

nn_min, nn_max = np.min(nn_vals), np.max(nn_vals)
num_nn = 10
nn_thresholds = np.linspace(nn_min, nn_max, num_nn)

# We'll compute up to dimension=2
max_dim = 2

# Initialize arrays: betti0, betti1, betti2
betti0_heatmap = np.zeros((num_ext, num_nn))
betti1_heatmap = np.zeros((num_ext, num_nn))
betti2_heatmap = np.zeros((num_ext, num_nn))

# --------------------------
# Step 4: Build Rips complexes, compute persistence, store Betti-k
# --------------------------
for i, ext_thresh in enumerate(ext_thresholds):
    for j, nn_thresh in enumerate(nn_thresholds):
        # Filter points whose filtration values are <= current thresholds
        indices = np.where((extinction_vals <= ext_thresh) & (nn_vals <= nn_thresh))[0]
        filtered_points = spatial_points[indices]

        # Handle degenerate cases
        if len(filtered_points) < 2:
            # Betti-0 = number of points, Betti-1 and Betti-2 = 0
            betti0_heatmap[i, j] = len(filtered_points)
            betti1_heatmap[i, j] = 0
            betti2_heatmap[i, j] = 0
            continue

        try:
            # Build Rips up to dimension=2, using nn_thresh as max edge length
            rips_complex = gd.RipsComplex(points=filtered_points, max_edge_length=nn_thresh)
            simplex_tree = rips_complex.create_simplex_tree(max_dimension=max_dim)

            # Compute persistence
            simplex_tree.compute_persistence()
            bnums = simplex_tree.betti_numbers()
            # bnums is a list [Betti-0, Betti-1, Betti-2], possibly shorter if dimension < 2
            betti0_heatmap[i, j] = bnums[0] if len(bnums) > 0 else 0
            betti1_heatmap[i, j] = bnums[1] if len(bnums) > 1 else 0
            betti2_heatmap[i, j] = bnums[2] if len(bnums) > 2 else 0

        except Exception as e:
            print(f"Error for ext_thresh={ext_thresh:.3f}, nn_thresh={nn_thresh:.3f}: {e}")
            betti0_heatmap[i, j] = np.nan
            betti1_heatmap[i, j] = np.nan
            betti2_heatmap[i, j] = np.nan

# --------------------------
# Step 5: Plot subplots for Betti-0, Betti-1, Betti-2
# --------------------------
fig, axes = plt.subplots(1, 3, figsize=(16, 5))

heatmaps = [betti0_heatmap, betti1_heatmap, betti2_heatmap]
titles = [r'Betti-0 (Connected Components)',
          r'Betti-1 (Loops)',
          r'Betti-2 (Voids)']

for ax, data, title in zip(axes, heatmaps, titles):
    im = ax.imshow(data,
                   aspect='auto',
                   origin='lower',
                   extent=[nn_thresholds[0], nn_thresholds[-1], ext_thresholds[0], ext_thresholds[-1]],
                   cmap='viridis')
    ax.set_title(title)
    ax.set_xlabel('Nearest Neighbor Threshold')
    ax.set_ylabel('Extinction Threshold')
    fig.colorbar(im, ax=ax)

plt.suptitle('Bifiltration Heatmaps for Betti-0, Betti-1, Betti-2', fontsize=14)
plt.tight_layout()
plt.savefig("Betti-heatmaps.png")
plt.show()
