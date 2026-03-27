"""
Settings for various modes, displays, etc.
"""

#### CTA mode ####

display_routes = ["Racine", "Ashland & Van Buren"] # which train/bus stations/stops to display

cta_refresh_seconds = 60 * 5 # not recommended < 3 minutes due to refresh speed and display lifespan

min_arrival_to_omit = 5 # minutes until arrival to omit if less than; useful to set as the minimum time to get to station/stop

enable_scheduled_display = True # whether to automatically switch to this mode during certain time periods
scheduled_intervals = [("7:00 AM", "7:30 AM")] # list[tuple[str, str]] of times to auto switch to; inclusion: [start, end)

#### Cats mode ###

image_dir = "./images" # directory of images to show
enable_shuffle = True # whether to shuffle images on display

enable_scheduled_shuffle = True # whether to refresh the image at the same time each day
scheduled_refresh_time = "9:00 PM" # when to cycle image each day; ignored if enable_scheduled_shuffle is False
shuffle_seconds = 60 * 5 # interval between image cycles; ignored if enable_scheduled_shuffle is True; not recommended < 3 minutes
