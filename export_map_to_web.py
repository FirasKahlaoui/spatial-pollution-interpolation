import plotly.graph_objects as go
import numpy as np
import pandas as pd
from scipy.interpolate import griddata
import os
import json

try:
    import h3
except ImportError:
    print("CRITICAL: You must install the 'h3' library to generate hexagons.")
    exit(1)

# --- 1. Load data ---
data_path = "output/mse_healed_data.csv"
if not os.path.exists(data_path):
    print(f"Error: Data file {data_path} not found.")
    exit(1)

df = pd.read_csv(data_path)

HM_COLS = {
    "Pb (ug/L)": "Heavy_Metals_Pb_ug_L",
    "Cd (ug/L)": "Heavy_Metals_Cd_ug_L",
    "Hg (ug/L)": "Heavy_Metals_Hg_ug_L",
}

# --- 2. WHO / China GB 3838-2002 safety thresholds ---
THRESHOLDS = {
    "Pb (ug/L)": {"safe": 10, "medium": 50},
    "Cd (ug/L)": {"safe": 1, "medium": 5},
    "Hg (ug/L)": {"safe": 0.06, "medium": 0.1},
}


def classify(value, col_label):
    t = THRESHOLDS[col_label]
    if value <= t["safe"]:
        return "Safe Zone"
    elif value <= t["medium"]:
        return "Medium Zone"
    else:
        return "Danger Zone"


def zone_color(zone):
    return {
        "Safe Zone": "#00cc66",
        "Medium Zone": "#ffcc00",
        "Danger Zone": "#ff3300",
    }.get(zone, "#888888")


# --- Generate Station Hover Texts and Colors ---
station_hovers_pb = []
station_hovers_cd = []
station_hovers_hg = []
station_hovers_overall = []
overall_station_colors = []
zone_priority = {"Safe Zone": 0, "Medium Zone": 1, "Danger Zone": 2}

for _, row in df.iterrows():
    pb, cd, hg = (
        row["Heavy_Metals_Pb_ug_L"],
        row["Heavy_Metals_Cd_ug_L"],
        row["Heavy_Metals_Hg_ug_L"],
    )
    pb_z, cd_z, hg_z = (
        classify(pb, "Pb (ug/L)"),
        classify(cd, "Cd (ug/L)"),
        classify(hg, "Hg (ug/L)"),
    )

    overall_zone = max([pb_z, cd_z, hg_z], key=lambda z: zone_priority[z])
    overall_station_colors.append(zone_color(overall_zone))

    city, station = row.get("City", "Unknown"), row.get("Monitoring_Station", "Unknown")

    station_hovers_pb.append(
        f"<b>{city} - {station} (Point)</b><br>"
        f"Lat: {row['Latitude']:.3f} deg  Lon: {row['Longitude']:.3f} deg<br>"
        f"-----------------------------<br>"
        f"<b>Lead (Pb):</b> {pb:.3f} ug/L  <- {pb_z}"
    )
    station_hovers_cd.append(
        f"<b>{city} - {station} (Point)</b><br>"
        f"Lat: {row['Latitude']:.3f} deg  Lon: {row['Longitude']:.3f} deg<br>"
        f"-----------------------------<br>"
        f"<b>Cadmium (Cd):</b> {cd:.3f} ug/L  <- {cd_z}"
    )
    station_hovers_hg.append(
        f"<b>{city} - {station} (Point)</b><br>"
        f"Lat: {row['Latitude']:.3f} deg  Lon: {row['Longitude']:.3f} deg<br>"
        f"-----------------------------<br>"
        f"<b>Mercury (Hg):</b> {hg:.4f} ug/L  <- {hg_z}"
    )
    station_hovers_overall.append(
        f"<b>{city} - {station} (Point)</b><br>"
        f"Lat: {row['Latitude']:.3f} deg  Lon: {row['Longitude']:.3f} deg<br>"
        f"-----------------------------<br>"
        f"<b>Lead (Pb):</b> {pb:.3f} ug/L  <- {pb_z}<br>"
        f"<b>Cadmium (Cd):</b> {cd:.3f} ug/L  <- {cd_z}<br>"
        f"<b>Mercury (Hg):</b> {hg:.4f} ug/L  <- {hg_z}<br>"
        f"-----------------------------<br>"
        f"<b>Overall: {overall_zone}</b>"
    )

# --- 3. Build the interpolated surface layers ---
lon_min, lon_max = df["Longitude"].min(), df["Longitude"].max()
lat_min, lat_max = df["Latitude"].min(), df["Latitude"].max()
pad_lon, pad_lat = (lon_max - lon_min) * 0.03, (lat_max - lat_min) * 0.03

grid_res = 120
lon_g = np.linspace(lon_min - pad_lon, lon_max + pad_lon, grid_res)
lat_g = np.linspace(lat_min - pad_lat, lat_max + pad_lat, grid_res)
LON_G, LAT_G = np.meshgrid(lon_g, lat_g)

pts = df[["Longitude", "Latitude"]].values
interp_grids = {}

print("Interpolating surfaces...")
for label, col in HM_COLS.items():
    z_vals = df[col].values
    z_interp = griddata(pts, z_vals, (LON_G, LAT_G), method="cubic")
    nan_mask = np.isnan(z_interp)
    if np.any(nan_mask):
        z_lin = griddata(pts, z_vals, (LON_G, LAT_G), method="linear")
        z_interp[nan_mask] = z_lin[nan_mask]
    nan_mask2 = np.isnan(z_interp)
    if np.any(nan_mask2):
        z_near = griddata(pts, z_vals, (LON_G, LAT_G), method="nearest")
        z_interp[nan_mask2] = z_near[nan_mask2]
    interp_grids[label] = z_interp

# --- 3.5 Group Interpolated Points into H3 Hexagons ---
print("Generating H3 Hexagonal GeoJSON grid...")
H3_RESOLUTION = 4

lats = LAT_G.flatten()
lons = LON_G.flatten()
pbs = interp_grids["Pb (ug/L)"].flatten()
cds = interp_grids["Cd (ug/L)"].flatten()
hgs = interp_grids["Hg (ug/L)"].flatten()

hex_data = {}
for lat, lon, pb, cd, hg in zip(lats, lons, pbs, cds, hgs):
    try:
        h = h3.latlng_to_cell(lat, lon, H3_RESOLUTION)
    except AttributeError:
        h = h3.geo_to_h3(lat, lon, H3_RESOLUTION)

    if h not in hex_data:
        hex_data[h] = {"lat": [], "lon": [], "pb": [], "cd": [], "hg": []}

    hex_data[h]["lat"].append(lat)
    hex_data[h]["lon"].append(lon)
    hex_data[h]["pb"].append(pb)
    hex_data[h]["cd"].append(cd)
    hex_data[h]["hg"].append(hg)

hex_features = []
hex_ids, hex_pbs, hex_cds, hex_hgs = [], [], [], []
hex_overall_z = []
hex_hovers = {"Pb (ug/L)": [], "Cd (ug/L)": [], "Hg (ug/L)": []}
hex_overall_hover = []

for h, vals in hex_data.items():
    avg_pb, avg_cd, avg_hg = (
        np.mean(vals["pb"]),
        np.mean(vals["cd"]),
        np.mean(vals["hg"]),
    )
    avg_lat, avg_lon = np.mean(vals["lat"]), np.mean(vals["lon"])

    pz, cz, hz = (
        classify(avg_pb, "Pb (ug/L)"),
        classify(avg_cd, "Cd (ug/L)"),
        classify(avg_hg, "Hg (ug/L)"),
    )
    oz = max([pz, cz, hz], key=lambda z: zone_priority[z])

    hex_ids.append(h)
    hex_pbs.append(avg_pb)
    hex_cds.append(avg_cd)
    hex_hgs.append(avg_hg)
    hex_overall_z.append(zone_priority[oz])

    # Hexagon hovers named "Interpolated Point"
    hex_hovers["Pb (ug/L)"].append(
        f"<b>Interpolated Point (Pb)</b><br>"
        f"Lat: {avg_lat:.3f} deg  Lon: {avg_lon:.3f} deg<br>"
        f"-----------------------------<br>"
        f"<b>Lead (Pb):</b> {avg_pb:.3f} ug/L  <- {pz}"
    )
    hex_hovers["Cd (ug/L)"].append(
        f"<b>Interpolated Point (Cd)</b><br>"
        f"Lat: {avg_lat:.3f} deg  Lon: {avg_lon:.3f} deg<br>"
        f"-----------------------------<br>"
        f"<b>Cadmium (Cd):</b> {avg_cd:.3f} ug/L  <- {cz}"
    )
    hex_hovers["Hg (ug/L)"].append(
        f"<b>Interpolated Point (Hg)</b><br>"
        f"Lat: {avg_lat:.3f} deg  Lon: {avg_lon:.3f} deg<br>"
        f"-----------------------------<br>"
        f"<b>Mercury (Hg):</b> {avg_hg:.4f} ug/L  <- {hz}"
    )
    hex_overall_hover.append(
        f"<b>Interpolated Point</b><br>"
        f"Lat: {avg_lat:.3f} deg  Lon: {avg_lon:.3f} deg<br>"
        f"-----------------------------<br>"
        f"<b>Lead (Pb):</b> {avg_pb:.3f} ug/L  <- {pz}<br>"
        f"<b>Cadmium (Cd):</b> {avg_cd:.3f} ug/L  <- {cz}<br>"
        f"<b>Mercury (Hg):</b> {avg_hg:.4f} ug/L  <- {hz}<br>"
        f"-----------------------------<br>"
        f"<b>Overall: {oz}</b>"
    )

    try:
        boundary = h3.cell_to_boundary(h)
    except AttributeError:
        boundary = h3.h3_to_geo_boundary(h)

    coords = [[[lon, lat] for lat, lon in boundary]]
    coords[0].append(coords[0][0])

    hex_features.append(
        {
            "type": "Feature",
            "id": h,
            "geometry": {"type": "Polygon", "coordinates": coords},
        }
    )

geojson_data = {"type": "FeatureCollection", "features": hex_features}

# --- 4. Build Plotly figure ---
fig = go.Figure()

colormaps = {"Pb (ug/L)": "Blues", "Cd (ug/L)": "Oranges", "Hg (ug/L)": "Purples"}
layer_maxes = {"Pb (ug/L)": 50, "Cd (ug/L)": 5, "Hg (ug/L)": 0.1}
z_arrays = {"Pb (ug/L)": hex_pbs, "Cd (ug/L)": hex_cds, "Hg (ug/L)": hex_hgs}

# Trace 0, 1, 2: Add Hexagon Mesh Layers for Individual Metals
for label in HM_COLS.keys():
    fig.add_trace(
        go.Choroplethmapbox(
            geojson=geojson_data,
            locations=hex_ids,
            z=z_arrays[label],
            colorscale=colormaps[label],
            zmin=0,
            zmax=layer_maxes[label],
            marker_opacity=0.6,
            marker_line_width=0,
            showscale=True,
            colorbar=dict(
                title=dict(text=label, font=dict(color="white")),
                thickness=14,
                x=0.02,
                y=0.5,
                len=0.6,
                tickfont=dict(color="white"),
            ),
            text=hex_hovers[label],
            hoverinfo="text",
            name=f"Hex Grid - {label}",
            visible=False,
        )
    )

# Trace 3: Add Hexagon Mesh Layer for Overall Mesh
fig.add_trace(
    go.Choroplethmapbox(
        geojson=geojson_data,
        locations=hex_ids,
        z=hex_overall_z,
        colorscale=[
            [0.0, "#00cc66"],
            [0.33, "#00cc66"],
            [0.33, "#ffcc00"],
            [0.66, "#ffcc00"],
            [0.66, "#ff3300"],
            [1.0, "#ff3300"],
        ],
        zmin=0,
        zmax=2,
        showscale=False,
        marker_opacity=0.45,
        marker_line_width=0,
        text=hex_overall_hover,
        hoverinfo="text",
        name="Overall Safety Mesh",
        visible=True,
    )
)

# Trace 4: Station Points for Pb
fig.add_trace(
    go.Scattermapbox(
        lat=df["Latitude"].tolist(),
        lon=df["Longitude"].tolist(),
        mode="markers",
        marker=dict(
            size=12,
            color=df["Heavy_Metals_Pb_ug_L"].tolist(),
            colorscale="Blues",
            cmin=0,
            cmax=layer_maxes["Pb (ug/L)"],
            showscale=False,
            opacity=1.0,
            symbol="circle",
        ),
        text=station_hovers_pb,
        hoverinfo="text",
        name="Stations - Pb",
        visible=False,
    )
)

# Trace 5: Station Points for Cd
fig.add_trace(
    go.Scattermapbox(
        lat=df["Latitude"].tolist(),
        lon=df["Longitude"].tolist(),
        mode="markers",
        marker=dict(
            size=12,
            color=df["Heavy_Metals_Cd_ug_L"].tolist(),
            colorscale="Oranges",
            cmin=0,
            cmax=layer_maxes["Cd (ug/L)"],
            showscale=False,
            opacity=1.0,
            symbol="circle",
        ),
        text=station_hovers_cd,
        hoverinfo="text",
        name="Stations - Cd",
        visible=False,
    )
)

# Trace 6: Station Points for Hg
fig.add_trace(
    go.Scattermapbox(
        lat=df["Latitude"].tolist(),
        lon=df["Longitude"].tolist(),
        mode="markers",
        marker=dict(
            size=12,
            color=df["Heavy_Metals_Hg_ug_L"].tolist(),
            colorscale="Purples",
            cmin=0,
            cmax=layer_maxes["Hg (ug/L)"],
            showscale=False,
            opacity=1.0,
            symbol="circle",
        ),
        text=station_hovers_hg,
        hoverinfo="text",
        name="Stations - Hg",
        visible=False,
    )
)

# Trace 7: Station Points for Overall
fig.add_trace(
    go.Scattermapbox(
        lat=df["Latitude"].tolist(),
        lon=df["Longitude"].tolist(),
        mode="markers",
        marker=dict(
            size=12,
            color=overall_station_colors,
            opacity=1.0,
            symbol="circle",
        ),
        text=station_hovers_overall,
        hoverinfo="text",
        name="Stations - Overall",
        visible=True,
    )
)

# --- 5. Layout ---
fig.update_layout(
    mapbox=dict(
        style="white-bg",
        layers=[
            dict(
                sourcetype="raster",
                source=["https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}"],
                below="traces",
            )
        ],
        center=dict(lat=35.5, lon=104.0),
        zoom=3.6,
    ),
    paper_bgcolor="#111111",
    plot_bgcolor="#111111",
    font=dict(color="white"),
    showlegend=False,
    margin=dict(l=0, r=0, t=0, b=0),
    autosize=True,
)

# Export to JSON
fig.write_json("docs/map_data.json")
print("Map data successfully exported to docs/map_data.json")
