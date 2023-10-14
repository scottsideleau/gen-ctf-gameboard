from geographiclib.geodesic import Geodesic
from tabulate import tabulate
import yaml


# Function to calculate a new point given:
#   starting point, distance, and bearing
def calculate_new_point(starting_point, distance_meters, bearing_degrees):
    geod = Geodesic.WGS84
    destination = geod.Direct(
        starting_point[0], starting_point[1], bearing_degrees, distance_meters
    )
    return (destination["lat2"], destination["lon2"])


# Function to format coordinates as decimal minutes
def format_decimal_minutes(coordinates):
    lat, lon = coordinates
    lat_degrees = int(lat)
    lat_minutes = (lat - lat_degrees) * 60
    lon_degrees = int(lon)
    lon_minutes = (lon - lon_degrees) * 60
    return (
        f"{lat_degrees}° {lat_minutes:.3f}'",
        f"{lon_degrees}° {lon_minutes:.3f}'",
    )


# Load input parameters from a YAML file
with open("config.yml", "r") as config_file:
    config = yaml.safe_load(config_file)

# Extract input parameters from the YAML configuration
start_lat = config["start"]["latitude"]
start_lon = config["start"]["longitude"]
start_bearing = config["start"]["bearing"]
build_bearing = config["gameboard"]["build_bearing"]
start_height = config["gameboard"]["height"]
start_width = config["gameboard"]["width"]
flag_offset = config["gameboard"]["flag_offset"]

# Evaluate build direction
if build_bearing == "cw":
    build_dir = 1
else:
    build_dir = -1

# Calculate gameboard vertices
vertices = []
vertex_labels = ["A", "B", "C", "D"]
angle = start_bearing

for label in vertex_labels:
    if label == "A":
        point = (start_lat, start_lon)
    else:
        distance = start_width if label in ["B", "D"] else start_height
        point = calculate_new_point(vertices[-1], distance, angle)
    vertices.append(point)
    angle += 90 * build_dir  # Rotate for the next point

# Calculate flag locations
flag_distance = flag_offset  # meters offset
flag_locations = []

for i, point in enumerate(vertices):
    next_point = vertices[(i + 1) % 4]
    flag_lat = (point[0] + next_point[0]) / 2
    flag_lon = (point[1] + next_point[1]) / 2
    flag_locations.append(
        calculate_new_point((flag_lat, flag_lon), flag_distance, angle)
    )

# Calculate the length of each side and identify the two longest sides
side_lengths = []
for i in range(4):
    next_point = vertices[(i + 1) % 4]
    side_length = Geodesic.WGS84.Inverse(
        vertices[i][0], vertices[i][1], next_point[0], next_point[1]
    )["s12"]
    side_lengths.append(side_length)

# Identify the two longest sides
sorted_lengths = sorted(
    enumerate(side_lengths), key=lambda x: x[1], reverse=True
)
longest_sides = [sorted_lengths[0][0], sorted_lengths[1][0]]

# Calculate and append midpoints of the two longest sides
midpoints = []
for side_index in longest_sides:
    start_point = vertices[side_index]
    end_point = vertices[(side_index + 1) % 4]
    mid_lat = (start_point[0] + end_point[0]) / 2
    mid_lon = (start_point[1] + end_point[1]) / 2
    midpoints.append((mid_lat, mid_lon))

# Generate and print tables
tables = []
table_headers = [
    "Location",
    "Latitude",
    "Longitude",
    "Latitude (DM)",
    "Longitude (DM)",
]
vertex_labels += ["Flag_1", "Flag_2", "Mid_1", "Mid_2"]

for label, point in zip(vertex_labels, vertices + flag_locations + midpoints):
    dm_lat, dm_lon = format_decimal_minutes(point)
    tables.append(
        [label, f"{point[0]:.6f}", f"{point[1]:.6f}", f"{dm_lat}", f"{dm_lon}"]
    )

# Print tables
print("Coordinates in Decimal Degrees:")
print(
    tabulate(
        [[row[0], row[1], row[2]] for row in tables],
        headers=["Location", "Latitude", "Longitude"],
        tablefmt="pretty",
        numalign="left",
    )
)

print("\nCoordinates in Decimal Minutes:")
print(
    tabulate(
        [[row[0], row[3], row[4]] for row in tables],
        headers=["Location", "Latitude (DM)", "Longitude (DM)"],
        tablefmt="pretty",
        numalign="left",
    )
)

# Write table to YAML files
with open("output.yml", "w") as dd_file:
    yaml.safe_dump(
        [
            {
                table_headers[0]: row[0],
                table_headers[1]: row[1],
                table_headers[2]: row[2],
            }
            for row in tables
        ],
        dd_file,
        sort_keys=False,
    )
