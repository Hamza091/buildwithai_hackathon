import json

# Load the previously updated JSON file
with open("updated_biking_events_with_interests.json", "r") as file:
    biking_events = json.load(file)

# Predefined latitude and longitude for each location (mock data for demonstration)
# location_coordinates = {
#     "Boggs Demonstration State Forest, Cobb, California": [38.8355, -122.7164],
#     "Sonoma County Fairgrounds, Santa Rosa, CA": [38.4375, -122.7144],
#     "Golden Gate Park, San Francisco, California": [37.7690, -122.4835],
#     "Lake Tahoe, California/Nevada": [39.0968, -120.0324],
#     "Mt. Tamalpais State Park, Mill Valley, CA": [37.9239, -122.5965],
#     "Monterey, California": [36.6002, -121.8947],
#     "Death Valley National Park, California": [36.5054, -117.0794],
#     "Yosemite National Park, California": [37.8651, -119.5383],
#     "Santa Monica, California": [34.0195, -118.4912],
#     "Napa Valley, California": [38.5025, -122.2654],
#     # Add more predefined coordinates as needed
# }
location_coordinates = {
    "Santa Cruz, California": [36.9741, -122.0308],
    "Boulder, Colorado": [40.015, -105.2705],
    "Moab, Utah": [38.5733, -109.5498],
    "Sedona, Arizona": [34.8697, -111.7609],
    "Tahoe National Forest, California": [39.3300, -120.2415],
    # Add more predefined coordinates as needed
}

# Add coordinates to each event based on the location
for event in biking_events:
    location = event["event"]["location"]
    print(location)
    coordinates = location_coordinates.get(location, [0, 0])  # Default to [0, 0] if not found
    event["event"]["coordinates"] = {"latitude": coordinates[0], "longitude": coordinates[1]}

# Save the updated JSON file with coordinates
updated_file_with_coordinates_path = "updated_biking_events_with_coordinates.json"
with open(updated_file_with_coordinates_path, "w") as updated_file:
    json.dump(biking_events, updated_file, indent=4)
