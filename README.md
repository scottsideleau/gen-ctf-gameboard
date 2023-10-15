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
