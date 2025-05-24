"""
Provides functions to build and export a Folium map based on IP geolocation data.
"""

from typing import Dict, Optional, List
import os
import folium
from folium.plugins import MarkerCluster


def create_base_map(initial_location: Optional[List[float]] = None,
                    zoom_start: int = 2) -> folium.Map:
    """
    Create a Folium Map with the specified initial location and zoom level.
    """
    if initial_location is None:
        initial_location = [20.0, 0.0]
    return folium.Map(location=initial_location,
                      zoom_start=zoom_start,
                      control_scale=True)


def add_tile_layers(map_obj: folium.Map) -> None:
    """
    Add custom tile layers to the map (terrain, toner, dark matter).
    """
    folium.TileLayer(
        tiles="Cartodb Positron",
        attr="Map tiles by Cartodb Positron, CC BY 3.0 — Data © OpenStreetMap contributors",
        name="Cartodb Positron",
        control=True
    ).add_to(map_obj)

    folium.TileLayer(
        tiles="CartoDB dark_matter",
        attr="© OpenStreetMap contributors © CARTO",
        name="CartoDB Dark Matter",
        control=True
    ).add_to(map_obj)


def add_marker_cluster(map_obj: folium.Map,
                       ip_info: Dict[str, 'IPInfoRecord']) -> None:
    """
    Add clustered markers to the map for each IP location.
    """
    cluster = MarkerCluster(name="IP Markers").add_to(map_obj)
    for domain, record in ip_info.items():
        if not getattr(record, 'loc', None):
            continue
        try:
            lat_str, lon_str = record.loc.split(',')
            latitude, longitude = float(lat_str), float(lon_str)
        except (ValueError, AttributeError):
            continue

        popup = f"<strong>{domain}</strong><br>{record.city}<br>{record.org}"
        color = 'red' if record.country == 'US' else 'green'
        folium.Marker(
            location=[latitude, longitude],
            popup=popup,
            tooltip=record.org,
            icon=folium.Icon(color=color)
        ).add_to(cluster)


def add_layer_control(map_obj: folium.Map) -> None:
    """
    Add layer control widget to toggle map layers and clusters.
    """
    folium.LayerControl(collapsed=False).add_to(map_obj)


def build_map(ip_info_map: Dict[str, 'IPInfoRecord']) -> folium.Map:
    """
    Full pipeline: fetch IP data, create a base map, add layers and markers.
    """
    map_obj = create_base_map()
    add_tile_layers(map_obj)
    add_marker_cluster(map_obj, ip_info_map)
    add_layer_control(map_obj)
    return map_obj


def export_map(map_obj: folium.Map, filename: str = "all_locations_map.html") -> None:
    """
    Save the map to an HTML file in the parent directory.
    """
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    exported_dir = os.path.join(project_root, "exported")
    os.makedirs(exported_dir, exist_ok=True)
    file_path = os.path.join(exported_dir, filename)
    map_obj.save(file_path)
    print(f"   ✅ Saved map to {file_path}")
