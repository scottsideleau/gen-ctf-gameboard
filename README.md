# gen-ctf-gameboard
Generate lat/long coordinates for a capture-the-flag gameboard; including flag locations.

## Configuration
Modify key parameters in config.yml before executing; including, but not limited to:

* start
    * lat: Latitude of Point A in decimal degrees
    * long: Longitude of Point A in decimal degrees
    * brg: Bearing along the build direction
* gameboard
    * length: Length of the gameboard in meters
    * width: Width of the gameboard in meters
    * build_dir: Build direction (default: counterclockwise)
    * flag_offset: Distance to offset the flag in meters

## Counterclockwise (Default) Point Labeling Guide
![Generate CTF Gameboard (CCW)](images/gen-ctf-gameboard.png#gh-light-mode-only)
![Generate CTF Gameboard (CCW)](images/gen-ctf-gameboard-dark.png#gh-dark-mode-only)

## Clockwise Point Labeling Guide
![Generate CTF Gameboard (CW)](images/gen-ctf-gameboard-cw.png#gh-light-mode-only)
![Generate CTF Gameboard (CW)](images/gen-ctf-gameboard-cw-dark.png#gh-dark-mode-only)

## Output
Produces coordinates for all indicated points in:

* decimal degrees
    * for use in other environments
* decimal minutes
    * for use with chart navigation software (i.e. on boats)

Coordinates are pretty printed to 'stdout' and published to a YAML file (output.yml).

### Example Output
The results printed to 'stdout' using the example 'config.yml' parameters are:

	Coordinates in Decimal Degrees:
	+----------+------------+------------+
	| Location |  Latitude  | Longitude  |
	+----------+------------+------------+
	|    A     | -35.122924 | 150.710536 |
	|    B     | -35.122460 | 150.711208 |
	|    C     | -35.121356 | 150.710080 |
	|    D     | -35.121819 | 150.709408 |
	|  Mid_1   | -35.121908 | 150.710644 |
	|  Mid_2   | -35.122372 | 150.709972 |
	|  Flag_1  | -35.121726 | 150.709885 |
	|  Flag_2  | -35.122554 | 150.710731 |
	+----------+------------+------------+

	Coordinates in Decimal Minutes:
	+----------+---------------+----------------+
	| Location | Latitude (DM) | Longitude (DM) |
	+----------+---------------+----------------+
	|    A     | -35° -7.375'  |  150° 42.632'  |
	|    B     | -35° -7.348'  |  150° 42.672'  |
	|    C     | -35° -7.281'  |  150° 42.605'  |
	|    D     | -35° -7.309'  |  150° 42.564'  |
	|  Mid_1   | -35° -7.314'  |  150° 42.639'  |
	|  Mid_2   | -35° -7.342'  |  150° 42.598'  |
	|  Flag_1  | -35° -7.304'  |  150° 42.593'  |
	|  Flag_2  | -35° -7.353'  |  150° 42.644'  |
	+----------+---------------+----------------+
