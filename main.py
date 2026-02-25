import time
import datetime
import random
from PIL import Image, ImageDraw

# from inky.auto import auto

import data_parsers
import display_helpers

# inky_display = auto(ask_user=True, verbose=True)

station_data = {
    "staNm": ["Racine"],
    "staId": [40470],
    "staData": []
}

data_parsers.get_and_parse_data(station_data)

if __name__ == "__main__":
    display_helpers.draw_arrivals(station_data["staData"][0])
