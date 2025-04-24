# 🌌 **TDA Galactic Extinction _r_** &nbsp;![Python](https://img.shields.io/badge/python-3.10+-blue) ![License](https://img.shields.io/github/license/dylan-wolf/TDA_galactic_extinction_r)

> **Multidimensional persistent homology meets interstellar dust.**  
> Dive into the code that turns Sloan Digital Sky Survey data into beautiful Betti-number heat-maps and fresh insights about how dust shapes our view of the Milky Way.  

---

## ✨ What’s inside
* **4-D point cloud** `(RA, Dec, redshift, extinction_r)` sampled from SDSS.
* **Single-parameter TDA** with Gudhi to explore the raw 3-D spatial structure.
* **Custom 2-parameter bifiltration** (`extinction` × `nearest-neighbor distance`) with heat-map visualisations that expose clusters (β₀) and loops (β₁) approximating rank invariants. 
* Lightweight, reproducible Python scripts—no heavyweight workflow managers required.

---

## 📂 Repository map

| Path | Purpose |
|------|---------|
| `assets/SDSS` | Example SQL queries and outputs to SDSS. |
|`assets/images` | Example outputs of the program. |
|`code/image_generator` | Generates example simplicial complex images used in paper. |
| `code/initial_review/variation_heat_map.py` | Quick EDA – scatter, hexbin, histograms of **extinction_r**.|
| `code/initial_review/tda_spatial_gudhi.py` | Vietoris–Rips, persistence diagrams/barcodes on **[RA,Dec,z]**. |
| `code/mutlidimensional/tda_bifilter_points_generator.py` | Builds bifiltration input grid (extinction + NN-distance). |
| `code/multidimensional/bifiltration_analysis.py` | Runs 2-D persistence, spits out β₀/β₁/β₂ heat-maps. |
| `code/output_data` | Example output data of `tda_bifiltration_points_generator.py`. |
| `paper/` | Draft PDF of the companion research article. |

---

## Quick-start

```bash
# 1. Clone & create a fresh environment
git clone https://github.com/dylan-wolf/TDA_galactic_extinction_r.git
cd TDA_galactic_extinction_r
python -m venv .venv && source .venv/bin/activate

# 2. Install requirements
pip install -r requirements.txt   

# 3. Drop your SDSS CSV in ./data   (or use the included sample)
# 4. Run a first look
python variation_heat_map.py

# 5. Ready for topology?
python tda_spatial_gudhi.py          # 1-parameter analysis
python tda_bifilter_points_generator.py
python bifiltration_analysis.py      # 2-parameter Betti heat-maps

```
---

## 🖼 Sneak peek

![β₀/β₁ heat-map teaser](/assets/images/bifiltration_output/first_Betti-heatmap.png)

> Clusters merge rapidly with increasing spatial radius while β₁ loops bloom at intermediate extinction thresholds—hinting at ring-like dust structures in the surveyed sky.

---


If you use this code, please cite:

```latex
@unpublished{Wolf2025,
  author    = {Dylan Wolf},
  title     = {Using Topological Data Analysis to Analyze Galactic Extinction Rates},
  note      = {May 2025, available in this repository}
}
```

---

## Acknowledgements
* **SDSS Collaboration** – for the open-access sky survey data.
* **Gudhi** & **RIVET** teams – for making computational topology approachable.

---

Made by **Dylan Wolf**.
