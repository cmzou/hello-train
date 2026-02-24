import time
import random
from PIL import Image

from inky.auto import auto

inky = auto(ask_user=True, verbose=True)

image_paths = ["hudson.png", "hudson2.png", "hudson3.png"]

def display_images():
    while True:
        image_path = random.choice(image_paths)
        image = Image.open(image_path)
        resizedimage = image.resize(inky.resolution)
        inky.set_image(resizedimage)
        inky.show()
        time.sleep(5*60)

def main():
    display_images()


if __name__ == "__main__":
    main()
