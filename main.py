import time
import datetime
import random
from PIL import Image, ImageDraw

from inky.auto import auto

inky_display = auto(ask_user=True, verbose=True)

image_paths = ["hudson.png", "hudson2.png", "hudson3.png"]

def get_current_time() -> str:
    current_time = datetime.datetime.today()
    return current_time.strftime("%Y/%m/%d %H:%M:%S")

def display_images():
    while True:
        image_path = random.choice(image_paths)
        image = Image.open("./images/" + image_path)
        resizedimage = image.resize(inky_display.resolution)

        draw = ImageDraw.Draw(resizedimage)
        draw.text((0, 0), f"Last Updated: {get_current_time()}", inky_display.BLACK)

        inky_display.set_image(resizedimage)
        inky_display.show()
        time.sleep(5*60)

def main():
    display_images()


if __name__ == "__main__":
    main()
