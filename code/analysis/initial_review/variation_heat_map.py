import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pandas as pd
import numpy as np

# Load and clean the data
df = pd.read_csv('Skyserver_SQL3_16_2025 8_52_53 PM.csv', dtype=str)
df.columns = df.columns.str.strip()
df = df.apply(pd.to_numeric, errors='coerce')
df.dropna(subset=['ra', 'dec', 'redshift', 'extinction_r'], inplace=True)

# Strip column names again 
df.columns = df.columns.str.strip()

### 1. Log-normalized scatter plot 
plt.figure(figsize=(10, 6))
norm = mcolors.LogNorm(vmin=df['extinction_r'].min(), vmax=df['extinction_r'].max())
sc = plt.scatter(df['ra'], df['dec'], c=df['extinction_r'], cmap='inferno', norm=norm, s=10, alpha=0.6)
plt.colorbar(sc, label='Extinction (r-band, log scale)')
plt.title('Log-Scaled Spatial Variation of Extinction_r in RA-Dec Region')
plt.xlabel('Right Ascension (degrees)')
plt.ylabel('Declination (degrees)')
plt.grid(True)
plt.tight_layout()
plt.savefig('Log-Scaled_Spatial_Variation.png')
plt.show()

### 2. Hexbin plot (shows spatial density + extinction variation)
plt.figure(figsize=(10, 6))
hb = plt.hexbin(df['ra'], df['dec'], C=df['extinction_r'], reduce_C_function=np.mean,
                gridsize=80, cmap='inferno')
plt.colorbar(hb, label='Mean Extinction (r-band)')
plt.title('Hexbin Plot of Extinction_r across RA-Dec')
plt.xlabel('Right Ascension (degrees)')
plt.ylabel('Declination (degrees)')
plt.grid(True)
plt.tight_layout()
plt.savefig('Hexbin_Plot.png')
plt.show()

### 3. Histogram of extinction_r distribution
plt.figure(figsize=(8, 5))
plt.hist(df['extinction_r'], bins=50, color='gray', edgecolor='black')
plt.title('Distribution of Extinction_r Values')
plt.xlabel('Extinction (r-band)')
plt.ylabel('Number of Objects')
plt.grid(True)
plt.tight_layout()
plt.savefig("Distribution_of_Extinction_r.png")
plt.show()

### 4. Breaking down extinction and showing median redshift



# Bin extinction_r
df['ext_bin'] = pd.cut(df['extinction_r'], bins=np.linspace(df['extinction_r'].min(), df['extinction_r'].max(), 25))

# Group and compute median
median_redshift = df.groupby('ext_bin')['redshift'].median()
bin_centers = [interval.mid for interval in median_redshift.index]

# Plot trend
plt.figure(figsize=(8, 5))
plt.plot(bin_centers, median_redshift.values, marker='o', color='darkred')
plt.title('Median Redshift per Extinction Bin')
plt.xlabel('Extinction (r-band)')
plt.ylabel('Median Redshift')
plt.grid(True)
plt.tight_layout()
plt.savefig("Median_Redshift.png")
plt.show()


'''
For most extinction values (<0.18), the median redshift stays relatively flat, around ~0.10–0.11. This is expected — foreground dust isn't tied to distance.
But then at higher extinction_r values (>0.18), the median redshift unexpectedly jumps up, peaking around 0.15 — before dropping again.
THis is due to not having any high extinction_r values.
'''
