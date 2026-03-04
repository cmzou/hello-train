"""
Settings for various modes, displays, etc.
"""


#### CTA mode ####

display_train_stations = ["Racine"] # which train stations to display
display_bus_stops = ["Ashland & Van Buren"] # which bus stops to display

cta_refresh_seconds = 60 * 5 # not recommended < 3 minutes due to refresh speed and display lifespan

#### Cats mode ###

image_dir = "./images" # directory of images to show
enable_shuffle = True # whether to shuffle images on display

enable_scheduled_shuffle = True
scheduled_refresh_time = "9:00 PM" # when to cycle image each day; ignored if enable_scheduled_shuffle is False
shuffle_seconds = 60 * 5 # interval between image cycles; ignored if enable_scheduled_shuffle is True

