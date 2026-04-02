# End User

## Usage

* A: CTA mode
* B: Cats mode
* C: News mode
* D: Mode specific operations

Pushing the button corresponding to the current mode will refresh the mode.

### Mode Specific Operations

#### CTA Mode

Toggle saved routes

## Settings

* select which train/bus lines to display
* enable/disable automatic switch to CTA mode
* enable/disable cats mode shuffle

## Cats Mode

Any image included in the `./images/` folder will be used in Cats Mode.

# Development

## Usage

```sh
uv run main.py
```

# References

1. Inky Impression 4" resolution is 640 x 400.
1. Map IDs (AKA Station IDs for trains) can be retrieved from the [City of Chicago](https://data.cityofchicago.org/resource/8pix-ypme.json?$query=SELECT%0A%20%20%60stop_id%60%2C%0A%20%20%60direction_id%60%2C%0A%20%20%60stop_name%60%2C%0A%20%20%60station_name%60%2C%0A%20%20%60station_descriptive_name%60%2C%0A%20%20%60map_id%60%2C%0A%20%20%60ada%60%2C%0A%20%20%60red%60%2C%0A%20%20%60blue%60%2C%0A%20%20%60g%60%2C%0A%20%20%60brn%60%2C%0A%20%20%60p%60%2C%0A%20%20%60y%60%2C%0A%20%20%60pnk%60%2C%0A%20%20%60o%60%2C%0A%20%20%60location%60%0AORDER%20BY%20%60station_name%60%20ASC%20NULL%20LAST).
1. Stop IDs (for buses) can be retrieved from https://www.ctabustracker.com/bustime/api/v3/getstops endpoint.
