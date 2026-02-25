import datetime
import pandas as pd
from PIL import Image, ImageDraw

from inky.auto import auto

inky_display = auto(ask_user=True, verbose=True)

def get_current_time() -> str:
    current_time = datetime.datetime.today()
    return current_time.strftime("%Y/%m/%d %H:%M:%S")

def draw_arrivals(arrivals_data: pd.DataFrame) -> None:
    # Create new PIL image with a black background
    image = Image.new("P", (inky_display.width, inky_display.height), inky_display.BLACK)
    draw = ImageDraw.Draw(image)

    draw.rectangle((320, 320, 300, 300), fill=inky_display.BLUE)
    draw.text((0, 0), f"Last Updated: {get_current_time()}", inky_display.BLACK)

    inky_display.set_image(image)
    inky_display.show()
