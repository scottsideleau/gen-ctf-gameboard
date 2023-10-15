#! /bin/python3

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


# Function to generate geodesic goodinates for CTF gameboard:
#   pretty table printing (DD and DMS), output.yml (DD)
def main():
    # Load input parameters from a YAML file
    with open("config.yml", "r") as config_file:
        config = yaml.safe_load(config_file)

    # Extract input parameters from the YAML configuration
    start_lat = config["start"]["lat"]
    start_lon = config["start"]["long"]
    start_brg = config["start"]["brg"]
    build_dir = config["gameboard"]["build_dir"]
    board_length = config["gameboard"]["length"]
    build_width = config["gameboard"]["width"]
    flag_offset = config["gameboard"]["flag_offset"]

    # Evaluate build direction
    if build_dir == "cw":
        build_sign = 1
    else:
        build_sign = -1

    # Calculate gameboard vertices
    vertices = []
    vertex_labels = ["A", "B", "C", "D"]
    angle = start_brg

    for label in vertex_labels:
        if label == "A":
            point = (start_lat, start_lon)
        else:
            distance = build_width if label in ["B", "D"] else board_length
            point = calculate_new_point(vertices[-1], distance, angle)
        vertices.append(point)
        angle += 90 * build_sign  # Rotate for the next point

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

    # Identify the two shortest sides
    shortest_sides = [sorted_lengths[2][0], sorted_lengths[3][0]]

    # Calculate flag locations
    flag_distance = flag_offset  # meters offset
    flags = []
    for side_index in shortest_sides:
        start_point = vertices[side_index]
        end_point = vertices[(side_index + 1) % 4]
        mid_lat = (start_point[0] + end_point[0]) / 2
        mid_lon = (start_point[1] + end_point[1]) / 2
        angle = start_brg
        if build_dir == "cw":
            if side_index == shortest_sides[0]:
                angle += 180.0
        else:  # ccw
            if side_index == shortest_sides[1]:
                angle += 180.0
        flags.append(
            calculate_new_point((mid_lat, mid_lon), flag_distance, angle)
        )

    # Generate tables for printing/writing
    tables = []

    vertex_labels += ["Mid_1", "Mid_2", "Flag_1", "Flag_2"]
    for label, point in zip(vertex_labels, vertices + midpoints + flags):
        dm_lat, dm_lon = format_decimal_minutes(point)
        tables.append(
            [
                label,
                f"{point[0]:.6f}",
                f"{point[1]:.6f}",
                f"{dm_lat}",
                f"{dm_lon}",
            ]
        )

    # Print tables
    print("Coordinates in Decimal Degrees:")
    print(
        tabulate(
            [[row[0], row[1], row[2]] for row in tables],
            headers=["Location", "Latitude", "Longitude"],
            tablefmt="pretty",
            numalign="decimal",
        )
    )

    print("\nCoordinates in Decimal Minutes:")
    print(
        tabulate(
            [[row[0], row[3], row[4]] for row in tables],
            headers=["Location", "Latitude (DM)", "Longitude (DM)"],
            tablefmt="pretty",
            numalign="decimal",
        )
    )

    # Write table to YAML files
    table_headers = [
        "Location",
        "Latitude",
        "Longitude",
        "Latitude (DM)",
        "Longitude (DM)",
    ]
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


if __name__ == "__main__":
    main()
