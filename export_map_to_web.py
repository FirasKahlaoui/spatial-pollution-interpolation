import plotly.graph_objects as go
import numpy as np
import pandas as pd
from scipy.interpolate import griddata
import os
import json

# --- 1. Load data ---
# We assume this script is run from the root directory
data_path = 'output/mse_healed_data.csv'
if not os.path.exists(data_path):
    print(f"Error: Data file {data_path} not found.")
    exit(1)

df = pd.read_csv(data_path)

HM_COLS = {
    'Pb (ug/L)': 'Heavy_Metals_Pb_ug_L',
    'Cd (ug/L)': 'Heavy_Metals_Cd_ug_L',
    'Hg (ug/L)': 'Heavy_Metals_Hg_ug_L',
}

# --- 2. WHO / China GB 3838-2002 safety thresholds ---
THRESHOLDS = {
    'Pb (ug/L)': {'safe': 10,  'medium': 50},
    'Cd (ug/L)': {'safe': 1,   'medium': 5},
    'Hg (ug/L)': {'safe': 0.06, 'medium': 0.1},
}


def classify(value, col_label):
    t = THRESHOLDS[col_label]
    if value <= t['safe']:
        return 'Safe Zone'
    elif value <= t['medium']:
        return 'Medium Zone'
    else:
        return 'Danger Zone'


def zone_color(zone):
    return {'Safe Zone': '#00cc66',
            'Medium Zone': '#ffcc00',
            'Danger Zone': '#ff3300'}.get(zone, '#888888')


zones = []
hover_texts = []
dot_colors = []
zone_priority = {'Safe Zone': 0, 'Medium Zone': 1, 'Danger Zone': 2}

for _, row in df.iterrows():
    pb, cd, hg = row['Heavy_Metals_Pb_ug_L'], row['Heavy_Metals_Cd_ug_L'], row['Heavy_Metals_Hg_ug_L']
    pb_z, cd_z, hg_z = classify(
        pb, 'Pb (ug/L)'), classify(cd, 'Cd (ug/L)'), classify(hg, 'Hg (ug/L)')

    overall_zone = max([pb_z, cd_z, hg_z], key=lambda z: zone_priority[z])
    zones.append(overall_zone)
    dot_colors.append(zone_color(overall_zone))

    city, station = row.get('City', 'Unknown'), row.get(
        'Monitoring_Station', 'Unknown')
    text = (
        f"<b>{city} - {station}</b> (Station)<br>"
        f"Lat: {row['Latitude']:.3f} deg  Lon: {row['Longitude']:.3f} deg<br>"
        f"-----------------------------<br>"
        f"<b>Lead (Pb):</b> {pb:.3f} ug/L  <- {pb_z}<br>"
        f"<b>Cadmium (Cd):</b> {cd:.3f} ug/L  <- {cd_z}<br>"
        f"<b>Mercury (Hg):</b> {hg:.4f} ug/L  <- {hg_z}<br>"
        f"-----------------------------<br>"
        f"<b>Overall: {overall_zone}</b>"
    )
    hover_texts.append(text)

df['Zone'] = zones
df['DotColor'] = dot_colors
df['HoverText'] = hover_texts

# --- 3. Build the interpolated surface layers ---
lon_min, lon_max = df['Longitude'].min(), df['Longitude'].max()
lat_min, lat_max = df['Latitude'].min(),  df['Latitude'].max()
pad_lon, pad_lat = (lon_max - lon_min) * 0.03, (lat_max - lat_min) * 0.03

grid_res = 120
lon_g = np.linspace(lon_min - pad_lon, lon_max + pad_lon, grid_res)
lat_g = np.linspace(lat_min - pad_lat, lat_max + pad_lat, grid_res)
LON_G, LAT_G = np.meshgrid(lon_g, lat_g)

pts = df[['Longitude', 'Latitude']].values
interp_grids = {}

for label, col in HM_COLS.items():
    z_vals = df[col].values
    z_interp = griddata(pts, z_vals, (LON_G, LAT_G), method='cubic')
    nan_mask = np.isnan(z_interp)
    if np.any(nan_mask):
        z_lin = griddata(pts, z_vals, (LON_G, LAT_G), method='linear')
        z_interp[nan_mask] = z_lin[nan_mask]
    nan_mask2 = np.isnan(z_interp)
    if np.any(nan_mask2):
        z_near = griddata(pts, z_vals, (LON_G, LAT_G), method='nearest')
        z_interp[nan_mask2] = z_near[nan_mask2]
    interp_grids[label] = z_interp

# Overall Zone calculation for grid
grid_pb = interp_grids['Pb (ug/L)'].flatten()
grid_cd = interp_grids['Cd (ug/L)'].flatten()
grid_hg = interp_grids['Hg (ug/L)'].flatten()

overall_grid_colors = []
overall_grid_hover = []

for i in range(len(grid_pb)):
    p, c, h = grid_pb[i], grid_cd[i], grid_hg[i]
    pz, cz, hz = classify(p, 'Pb (ug/L)'), classify(c,
                                                    'Cd (ug/L)'), classify(h, 'Hg (ug/L)')
    oz = max([pz, cz, hz], key=lambda z: zone_priority[z])
    overall_grid_colors.append(zone_color(oz))

    hover_str = (
        f"<b>Interpolated Surface (Overall)</b><br>"
        f"Lat: {LAT_G.flatten()[i]:.3f} deg  Lon: {LON_G.flatten()[i]:.3f} deg<br>"
        f"Pb: {p:.3f} | Cd: {c:.3f} | Hg: {h:.4f}<br>"
        f"<b>Status: {oz}</b>"
    )
    overall_grid_hover.append(hover_str)

# --- 4. Build Plotly figure ---
fig = go.Figure()

colormaps = {'Pb (ug/L)': 'Blues', 'Cd (ug/L)': 'Oranges',
             'Hg (ug/L)': 'Purples'}
layer_maxes = {'Pb (ug/L)': 50, 'Cd (ug/L)': 5, 'Hg (ug/L)': 0.1}

for label in list(HM_COLS.keys()):
    z_grid = interp_grids[label].flatten()
    hover_surface = [
        f"<b>Interpolated {label}</b><br>Value: {val:.4f}<br>Lat: {lat:.3f} deg  Lon: {lon:.3f} deg"
        for val, lat, lon in zip(z_grid, LAT_G.flatten(), LON_G.flatten())
    ]
    fig.add_trace(go.Scattermapbox(
        lat=LAT_G.flatten().tolist(),
        lon=LON_G.flatten().tolist(),
        mode='markers',
        marker=dict(
            size=5,
            color=z_grid.tolist(),
            colorscale=colormaps[label],
            showscale=True,
            cmax=layer_maxes[label],
            opacity=0.6,
            colorbar=dict(
                title=dict(text=label, font=dict(color='white')),
                thickness=14,
                x=0.01 if label == 'Pb (ug/L)' else (0.08 if label ==
                                                     'Cd (ug/L)' else 0.15),
                y=0.5, len=0.6,
                tickfont=dict(color='white')
            ),
        ),
        text=hover_surface,
        hoverinfo='text',
        name=f'Interpolated Grid - {label}',
        visible=False
    ))

fig.add_trace(go.Scattermapbox(
    lat=LAT_G.flatten().tolist(),
    lon=LON_G.flatten().tolist(),
    mode='markers',
    marker=dict(
        size=5,
        color=overall_grid_colors,
        opacity=0.45,
    ),
    text=overall_grid_hover,
    hoverinfo='text',
    name='Overall Safety Mesh',
    visible=True
))

for zone_label, zone_col in [('Safe Zone', '#00cc66'), ('Medium Zone', '#ffcc00'), ('Danger Zone', '#ff3300')]:
    sub = df[df['Zone'] == zone_label]
    if not sub.empty:
        fig.add_trace(go.Scattermapbox(
            lat=sub['Latitude'].tolist(),
            lon=sub['Longitude'].tolist(),
            mode='markers',
            marker=dict(
                size=12,
                color=zone_col,
                opacity=1.0,
                symbol='circle',
            ),
            text=sub['HoverText'],
            hoverinfo='text',
            name=f"Current Station: {zone_label}",
        ))

# --- 5. Layout ---
fig.update_layout(
    mapbox=dict(
        style='white-bg',
        layers=[
            dict(
                sourcetype='raster',
                source=['https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}'],
                below='traces'
            )
        ],
        center=dict(lat=35.5, lon=104.0),
        zoom=3.6,
    ),
    paper_bgcolor='#111111',
    plot_bgcolor='#111111',
    font=dict(color='white'),
    legend=dict(
        title='<b>Map Setup</b>',
        bgcolor='rgba(30,30,30,0.85)', bordercolor='#555', borderwidth=1,
        x=1.0, y=1.0, xanchor='right', font=dict(size=12),
    ),
    margin=dict(l=0, r=0, t=0, b=0),
    height=750,
)

# Export to JSON
os.makedirs('webapp', exist_ok=True)
fig.write_json('webapp/map_data.json')
print("Map data successfully exported to webapp/map_data.json")
