import time
import datetime
import random
import os

from PIL import Image, ImageDraw

from inky.auto import auto

inky_display = auto(ask_user=True, verbose=True)

image_saturation = 0.75

image_dir = "./images"
image_paths = [os.path.join(image_dir, f) for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f))]

def get_current_time() -> str:
    current_time = datetime.datetime.today()
    return current_time.strftime("%Y/%m/%d %H:%M:%S")

def display_images():
    while True:
        image_path = random.choice(image_paths)
        image = Image.open(image_path)
        resizedimage = image.resize(inky_display.resolution)

        draw = ImageDraw.Draw(resizedimage)
        draw.text((0, 0), f"Last Updated: {get_current_time()}", inky_display.BLACK)

        inky_display.set_image(resizedimage, saturation=image_saturation)
        inky_display.show()
        time.sleep(5*60)

def main():
    display_images()


if __name__ == "__main__":
    main()
