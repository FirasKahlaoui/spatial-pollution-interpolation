# Spatial Pollution Interpolation 🌍

![Python](https://img.shields.io/badge/Python-3.x-blue)
![NumPy](https://img.shields.io/badge/NumPy-Scientific_Computing-orange)
![SciPy](https://img.shields.io/badge/SciPy-Numerical_Methods-green)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-purple)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-red)
![License](https://img.shields.io/badge/License-MIT-lightgrey)
![Status](https://img.shields.io/badge/Status-In_Progress-yellow)

---

## 📌 Project Overview

This project applies **numerical analysis techniques** to model the spatial distribution of water pollution using sparse monitoring station data.

Because pollution measurements are only available at discrete geographic points, numerical interpolation and approximation methods are used to reconstruct a **continuous pollution surface** over a given region.

The methodology is first validated using a **large scale Chinese water quality dataset (3,000 observations)** and then projected onto the **Gulf of Gabes (Tunisia)** to assess coastal pollution and heavy metal contamination.

---

## 🎯 Objectives

- Construct continuous pollution maps from discrete monitoring data  
- Apply bivariate interpolation and approximation methods  
- Validate numerical stability using a large scale dataset  
- Estimate pollutant concentration at arbitrary GPS coordinates  
- Identify critical contamination zones for environmental assessment  

---

## 🧮 Mathematical Framework

The project is based on concepts from **Numerical Analysis**, including:

- **Bivariate Interpolation**  
    Construction of a surface  
    $$z = f(x, y)$$
    where $x, y$ are geographic coordinates and $z$ is pollutant concentration.

- **Spline Approximation**  
    Piecewise polynomial surfaces to ensure smoothness and numerical stability.

- **Least Squares Regression**  
    Modeling pollution decay as a function of distance from industrial sources.

- **Numerical Integration (Extension)**  
    Estimation of total polluted areas exceeding safety thresholds.

---

## 📊 Datasets

### 1. China Dataset (Validation)

- ~3,000 monitoring stations
- Variables include pH, nutrients, heavy metals, and organic pollution
- Used for algorithms calibration and stress testing

### 2. Gabes Dataset (Target)

- 48 to 72 monitoring points
- Focus on heavy metals and industrial pollution
- Used for local environmental impact assessment

---

## 🧪 Key Variables

- Latitude, Longitude  
- Heavy Metals (Pb, Cd, Hg)  
- pH and water quality indicators  

These variables are used directly in the interpolation models.

---

## 🛠 Tools and Technologies

- **Language**: Python 3.x  
- **Libraries**:

  - NumPy
  - SciPy
  - Pandas
  - Matplotlib
- **Environment**:
  - Jupyter Notebook

---

## 📂 Project Structure

```bash
spatial-pollution-interpolation/
│
├── data/
│   ├── china/
│   └── gabes/
│
├── notebooks/
│   ├── data_exploration.ipynb
│   ├── interpolation_models.ipynb
│   └── validation.ipynb
│
├── src/
│   ├── interpolation/
│   ├── approximation/
│   └── visualization/
│
├── results/
│   ├── maps/
│   └── figures/
│
├── README.md
└── requirements.txt
```

---

## 📈 Expected Outputs

- Continuous 2D and 3D pollution maps  
- Predictive functions for pollutant estimation at any GPS coordinate  
- Quantitative assessment of polluted coastal zones  

---

## 🚀 Future Work

- Temporal modeling of pollution trends  
- Comparison of interpolation methods (RBF, IDW, splines)  
- Integration with GIS tools  
- Extension to other coastal regions  

---

## 📜 License

This project is licensed under the **MIT License**.  
You are free to use, modify, and distribute this work with proper attribution.

---

## 👥 Authors

**Firas Kahlaoui**  
Engineering Student  

**Ahmed Chaabane**  
Engineering Student  

---

## ⭐ Acknowledgments

This project is developed as part of a **Numerical Analysis** academic study with applications in environmental modeling and coastal pollution assessment.
