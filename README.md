# China Water Pollution Spatial Interpolation & Mapping

![Python](https://img.shields.io/badge/Python-3.x-blue)
![NumPy](https://img.shields.io/badge/NumPy-Scientific_Computing-orange)
![SciPy](https://img.shields.io/badge/SciPy-Numerical_Methods-green)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-purple)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-red)
![License](https://img.shields.io/badge/License-MIT-lightgrey)
![Status](https://img.shields.io/badge/Status-In_Progress-yellow)

---
A comprehensive data science project focused on cleaning, interpolating, and visualizing water pollution data across China. This repository implements advanced reconstruction techniques to handle sensor anomalies and provides a comparative analysis of various spatial interpolation methods.

## 🚀 Overview

Monitoring water quality across a vast geographic area like China often results in sparse data or sensor noise (e.g., non-physical negative concentration values). This project addresses these challenges by:
1. **Data Healing**: Using Optimized Radial Basis Function (RBF) reconstruction to eliminate negative values while maintaining data fidelity.
2. **Comparison of Methods**: Evaluating Polynomial (Lagrange, Newton) vs. Spline vs. Linear interpolation.
3. **Interactive Visualization**: Creating 2D and 3D maps to represent pollution levels (Heavy Metals, pH, Ammonia, etc.) spatially.

## ✨ Key Features

- **High-Fidelity Reconstruction**: Phase-based RBF optimization with hyperparameter tuning (smooth, epsilon, basis function) to minimize Mean Squared Error (MSE).
- **Multiple Interpolation Algorithms**:
  - **1D/2D Polynomial**: Lagrange and Newton forms for mathematical analysis.
  - **Splines**: Cubic Spline and Piecewise Linear for smoother spatial transitions.
  - **RBF**: Multi-dimensional spatial interpolation.
- **3D Geospatial Mapping**: Leveraging Plotly for interactive 3D visualizations of pollution gradients over the map of China.
- **Anomaly Detection**: Automated styling and statistical summaries to highlight pollution spikes and sensor errors.

## 🛠 Technology Stack

- **Data Manipulation**: `pandas`, `numpy`
- **Scientific Computing**: `scipy`, `sympy`, `scikit-learn`
- **Visualization**: `matplotlib`, `seaborn`, `plotly`
- **Dashboard/Export**: Custom Python scripts for web-ready data export.

## 📁 Project Structure

```text
├── data/                       # Source CSV files (Input)
├── notebooks/                  # Jupyter notebooks for analysis
│   └── Final_Notebook.ipynb    # Main analysis and comparison
├── output/                     # Healed datasets and results
├── export_map_to_web.py        # Pipeline for web dashboard export
├── requirements.txt            # Project dependencies
└── run_dashboard.bat           # Utility to launch visualization
```

## ⚙️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/FirasKahlaoui/spatial-pollution-interpolation.git
   cd spatial-pollution-interpolation
   ```

2. **Set up a virtual environment** (recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 📊 Usage

### Analysis
Open the `notebooks/Final_Notebook.ipynb` to view the full pipeline from raw data ingestion to final interpolation comparisons.

### Dashboard Export
Run the export script to generate processed data for web visualizations:
```bash
python export_map_to_web.py
```

## 🧪 Methodology Highlights

### RBF Reconstruction
The project uses a two-phase approach for data cleaning:
- **Phase 1**: Grid search over RBF parameters on valid (non-negative) data points.
- **Phase 2**: Reconstruction of full dataset using the best configuration to "heal" non-physical values.

### Spline vs. Polynomial
The notebook demonstrates that while high-degree polynomials (Lagrange/Newton) are useful for exact local fits, **Cubic Splines** offer superior stability for spatial mapping by avoiding the Runge phenomenon (oscillations at edges).

## 👥 Authors

**Firas Kahlaoui**  
Engineering Student  
**Ahmed Chaabane**  
Engineering Student
  
---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
