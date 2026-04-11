import datetime
import random
import os

from PIL import Image

from config import mode_settings
from display import draw_backgrounds
from util import util

import logging

logger = logging.getLogger(__name__)

image_saturation = 0.75

displays = {}

"""
Given a refresh time of the form H:MM P, calculate the number of seconds until the next refresh.
"""
def calc_time_until_refresh(refresh_time: str) -> int:
    current_datetime = datetime.datetime.today()
    current_date = current_datetime.strftime("%Y/%m/%d")
    refresh_datetime = datetime.datetime.strptime(current_date + " " + refresh_time, "%Y/%m/%d %I:%M %p")

    if refresh_datetime > current_datetime: # hasn't passed refresh time
        time_until_refresh = refresh_datetime - current_datetime
    else: # passed refresh time, calculate the next available one
        next_datetime = current_datetime + datetime.timedelta(days=1)
        next_datetime = next_datetime.replace(hour=refresh_datetime.hour, minute=refresh_datetime.minute)

        time_until_refresh = next_datetime - current_datetime

    return time_until_refresh.total_seconds()

class ImageDisplay:
    """
    Params:
        shuffle_type: how should the images be set; accepted values: sequential, random (default)
    """
    def __init__(self, images: str | list[str], shuffle_type: str="random") -> None:
        self.image_paths = self.get_images_to_display(images)
        self.shuffle_type = shuffle_type
        self.current_image_i = -1
        self.set_current_image()
        
    """
    Resolve the given images to display. Does NOT check if it is a valid image file.

    Params:
        images: either the path to a directory full of images to display, a single image, or a list of image paths

    Returns:
        a list of image paths to display
    """
    def get_images_to_display(self, images: str | list[str]) -> list[str]:
        if isinstance(images, list):
            image_paths = images
        elif os.path.isdir(images):
            image_paths = [os.path.join(images, f) for f in os.listdir(images) if os.path.isfile(os.path.join(images, f))]
        elif os.path.isfile(images):
            image_paths = [images]
        else:
            raise ValueError(f"Unknown image passed to display: {images}")

        if len(image_paths) == 0:
            raise ValueError("Empty list of images given.")

        return image_paths

    """
    Set the current image from the given images
    """
    def set_current_image(self):
        if self.shuffle_type == "random":
            self.current_image = random.choice(self.image_paths)
        elif self.shuffle_type == "sequential":
            if self.current_image_i == -1:
                self.current_image = self.image_paths[0]
                self.current_image_i = 0
            else:
                next_image_i = util.get_next_i_in_list(self.current_image_i, self.image_paths)
                self.current_image = self.image_paths[next_image_i]
                self.current_image_i = next_image_i
        else:
            raise ValueError(f"Unknown shuffle_type given: {self.shuffle_type}")

    """
    Display the current image
    """
    def display_current_image(self, inky_display):
        image = Image.open(self.current_image)
        resizedimage = image.resize(inky_display.resolution)

        resizedimage = draw_backgrounds.write_last_updated(resizedimage)

        inky_display.set_image(resizedimage, saturation=image_saturation)
        inky_display.show()

def setup():
    # Set up the error display first so that it'll always be available
    error_display = ImageDisplay("./images/special/error.png")
    displays["error"] = error_display

    cta_display = ImageDisplay("./ui/cta_ui.png")
    if mode_settings.enable_shuffle:
        cat_display = ImageDisplay(mode_settings.image_dir)
    else:
        cat_display = ImageDisplay(mode_settings.image_dir, shuffle_type="sequential")

    displays["cta"] = cta_display
    displays["cat"] = cat_display
