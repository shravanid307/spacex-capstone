import os
import folium
from folium.plugins import MarkerCluster
from folium import DivIcon
import pandas as pd
from math import sin, cos, sqrt, atan2, radians

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
MAPS_DIR = os.path.join(BASE_DIR, "maps")
os.makedirs(MAPS_DIR, exist_ok=True)

spacex_df = pd.read_csv(os.path.join(DATA_DIR, "spacex_launch_geo.csv"))

# Calculate haversine distance in km
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6373.0  # approximate radius of earth in km
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance

# Initialize Folium Map centered on US launch latitude/longitude
site_map = folium.Map(location=[28.562302, -80.577356], zoom_start=5)

# Launch site coordinates
launch_sites = spacex_df[['Launch Site', 'Lat', 'Long']].drop_duplicates()

# Add Circle and Marker for each Launch Site
for _, row in launch_sites.iterrows():
    site_coord = [row['Lat'], row['Long']]
    site_name = row['Launch Site']
    
    circle = folium.Circle(site_coord, radius=1000, color='#d35400', fill=True).add_to(site_map)
    marker = folium.map.Marker(
        site_coord,
        icon=DivIcon(
            icon_size=(20, 20),
            icon_anchor=(0, 0),
            html=f'<div style="font-size: 13pt; font-weight: bold; color: #d35400;">{site_name}</div>',
        )
    )
    site_map.add_child(circle)
    site_map.add_child(marker)

# Add Marker Cluster for all launches
marker_cluster = MarkerCluster().add_to(site_map)

for _, row in spacex_df.iterrows():
    launch_coord = [row['Lat'], row['Long']]
    is_success = row['class'] == 1
    color = 'green' if is_success else 'red'
    outcome_str = 'Success' if is_success else 'Failure'
    
    folium.Marker(
        location=launch_coord,
        icon=folium.Icon(color='white', icon_color=color),
        popup=f"Site: {row['Launch Site']}<br>Outcome: {outcome_str}<br>Flight: {row['Flight Number']}"
    ).add_to(marker_cluster)

# Proximity Analysis for CCAFS SLC-40
launch_site_lat = 28.563197
launch_site_lon = -80.576820

points_of_interest = {
    'Coastline': (28.56367, -80.56763, '#2A9D8F'),
    'Highway (Samuel Phillips Pkwy)': (28.56373, -80.57082, '#457B9D'),
    'Railroad (Titan IV)': (28.57205, -80.58527, '#F4A261'),
    'City (Titusville)': (28.61221, -80.80755, '#E76F51')
}

for name, (poi_lat, poi_lon, color) in points_of_interest.items():
    dist = calculate_distance(launch_site_lat, launch_site_lon, poi_lat, poi_lon)
    
    # Distance marker
    distance_marker = folium.Marker(
        [poi_lat, poi_lon],
        icon=DivIcon(
            icon_size=(20, 20),
            icon_anchor=(0, 0),
            html=f'<div style="font-size: 12pt; font-weight: bold; color: {color}; white-space: nowrap;">{name}: {dist:.2f} KM</div>',
        )
    )
    site_map.add_child(distance_marker)
    
    # Line
    lines = folium.PolyLine(
        locations=[[launch_site_lat, launch_site_lon], [poi_lat, poi_lon]],
        weight=2.5,
        color=color,
        dash_array='5, 5'
    )
    site_map.add_child(lines)

out_path = os.path.join(MAPS_DIR, "spacex_launch_site_map.html")
site_map.save(out_path)
print(f"Interactive Folium map saved to {out_path}")
