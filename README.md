# IP Geolocation and Threat Intelligence Mapping

This project retrieves browsing history, resolves domain names to IP addresses, fetches geolocation information, checks for threats, and visualizes the data on an interactive map using Folium. It helps analyze browsing behavior and detect potential threats based on geolocation data.

## Features:
- Fetch Browsing History: Retrieve browsing history from specified browsers (`Edge`, `Chrome`, or `Firefox`).
- Domain Resolution: Convert domain names to their respective IP addresses.
- Geolocation Data: Fetch geolocation information for each IP address.
- Threat Detection: Check IP addresses against a list of potentially malicious IPs.
- Interactive Map: Generate an interactive map that visualizes the IP locations and marks potential threats.
- Custom Tile Layers: Add different tile layers (like `Stamen Terrain`, `Toner`, and `CartoDB Dark Matter`) to the map for better visualization.
- Export Map: Export the map to an HTML file in the exported directory.

## Install:

First, install the following modules to work with the script(adding `python -m` works on my laptop since there was an unknown issue):
```
python -m pip install -r requirements.txt
python -m pip install -r requirements-dev.txt
```

## Usage:
To show the capabilities of the script use:
```
python src/main.py --help
```

To run the script and generate the map based on the browsing history of a selected browser (Edge, Chrome, or Firefox), use the following command:
```
python src/main.py --browser <browser_name> --max-domains <number_of_domains>
```

## Folder Structure
### src/
Contains all the main logic of the application:

- geolocate/: Logic for fetching and processing geolocation data.

- history/: Logic for fetching and parsing browser history.

- threat_intel/: Logic for checking IP addresses against threat intelligence.

- main.py: Entry point for the application that orchestrates the entire workflow.

- resolver.py: Logic for resolving domains.

### data/
Data that will be used during program runtime.

### exported/
Location of future generated maps based on browser selected by user.

### README.md
This file provides documentation for the project.

