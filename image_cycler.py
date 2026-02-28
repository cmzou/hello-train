import time
import datetime
import random
import os

from PIL import Image, ImageDraw

from inky.auto import auto

inky_display = auto(ask_user=True, verbose=True)

image_saturation = 0.75
sleep_seconds = 60 * 5

def get_current_time() -> str:
    current_time = datetime.datetime.today()
    return current_time.strftime("%Y/%m/%d %H:%M:%S")

"""
Resolve the given images to display. Does NOT check if it is a valid image file.

Params:
    images: either the path to a directory full of images to display, a single image, or a list of image paths

Returns:
    a list of image paths to display
"""
def get_images_to_display(images: str | list[str]) -> list[str]:
    if isinstance(images, list):
        image_paths = images
    elif os.path.isdir(images):
        image_paths = [os.path.join(images, f) for f in os.listdir(images) if os.path.isfile(os.path.join(images, f))]
    elif os.path.isfile(images):
        image_paths = [images]
    else:
        raise ValueError(f"Unknown image passed to display: {images}")

    return image_paths

"""
Display the given images
"""
def display_images(image_paths: list[str]) -> None:
    if len(image_paths) == 0:
        raise ValueError("Empty list of images given.")
    while True:
        image_path = random.choice(image_paths)
        image = Image.open(image_path)
        resizedimage = image.resize(inky_display.resolution)

        draw = ImageDraw.Draw(resizedimage)
        draw.text((0, 0), f"Last Updated: {get_current_time()}", inky_display.BLACK)

        inky_display.set_image(resizedimage, saturation=image_saturation)
        inky_display.show()
        if len(image_paths) == 0: # don't waste CPU cycles
            break
        time.sleep(sleep_seconds)

def main():
    display_images(get_images_to_display("./images"))

if __name__ == "__main__":
    main()
