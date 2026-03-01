import time
import datetime
import random
import os

from PIL import Image, ImageDraw

from inky.auto import auto

image_saturation = 0.75

displays = {}

def get_current_time() -> str:
    current_time = datetime.datetime.today()
    return current_time.strftime("%Y/%m/%d %H:%M:%S")

class ImageDisplay:
    def __init__(self, images: str | list[str]) -> None:
        self.image_paths = self.get_images_to_display(images)
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
        self.current_image = random.choice(self.image_paths)

    """
    Display the current image
    """
    def display_current_image(self, inky_display, last_update_xy=(0, 0), last_update_color=None, last_update_fnt=None):
        image = Image.open(self.current_image)
        resizedimage = image.resize(inky_display.resolution)

        draw = ImageDraw.Draw(resizedimage)

        draw.text(last_update_xy, f"Last Updated: {get_current_time()}", fill=last_update_color, font=last_update_fnt)

        inky_display.set_image(resizedimage, saturation=image_saturation)
        inky_display.show()

def setup():
    cta_display = ImageDisplay("./ui/cta_ui.png")
    cat_display = ImageDisplay("./images")

    displays["cta"] = cta_display
    displays["cat"] = cat_display
