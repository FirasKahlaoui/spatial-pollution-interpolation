# China Water Pollution Dataset

## Data Description Report

## 1. Dataset Overview

This dataset contains 3,000 water quality observations collected from multiple monitoring stations across different provinces and cities in China. Its main role in this project is to validate numerical interpolation and approximation methods before applying them to the Gulf of Gabes case study.

Each row represents one measurement taken at a specific geographic location and date, while the columns describe spatial, physical, chemical, biological, and pollution related indicators.

---

## 2. Spatial and Identification Columns

| Column Name | Description |
| --- | --- |
| Province | Administrative province where the monitoring station is located |
| City | City associated with the monitoring station |
| Monitoring_Station | Unique identifier of the monitoring station |
| Latitude | Geographic latitude of the monitoring station (decimal degrees) |
| Longitude | Geographic longitude of the monitoring station (decimal degrees) |
| Date | Date when the water sample was collected |

---

## 3. Physical Water Properties

| Column Name | Description |
| --- | --- |
| Water_Temperature_C | Water temperature measured in degrees Celsius |
| pH | Acidity or alkalinity level of the water |
| Dissolved_Oxygen_mg_L | Amount of dissolved oxygen in water (mg/L) |
| Conductivity_uS_cm | Electrical conductivity indicating ionic content (µS/cm) |
| Turbidity_NTU | Water clarity measurement based on suspended particles |

---

## 4. Nutrients and Chemical Compounds

| Column Name | Description |
| --- | --- |
| Nitrate_mg_L | Concentration of nitrate ions in water |
| Nitrite_mg_L | Concentration of nitrite ions in water |
| Ammonia_N_mg_L | Ammonia nitrogen concentration |
| Total_Phosphorus_mg_L | Total phosphorus concentration |
| Total_Nitrogen_mg_L | Total nitrogen concentration from all sources |

---

## 5. Organic Pollution Indicators

| Column Name | Description |
| --- | --- |
| COD_mg_L | Chemical Oxygen Demand indicating organic pollutant load |
| BOD_mg_L | Biological Oxygen Demand measuring biodegradable organic matter |

---

## 6. Heavy Metals

| Column Name | Description |
| --- | --- |
| Heavy_Metals_Pb_ug_L | Lead concentration measured in micrograms per liter |
| Heavy_Metals_Cd_ug_L | Cadmium concentration measured in micrograms per liter |
| Heavy_Metals_Hg_ug_L | Mercury concentration measured in micrograms per liter |

---

## 7. Biological Indicators

| Column Name | Description |
| --- | --- |
| Coliform_Count_CFU_100mL | Coliform bacteria count per 100 mL indicating microbial contamination |

---

## 8. Water Quality Assessment Outputs

| Column Name | Description |
| --- | --- |
| Water_Quality_Index | Composite index summarizing overall water quality |
| Pollution_Level | Categorical pollution classification |
| Remarks | Qualitative comments or alerts related to the measurement |
