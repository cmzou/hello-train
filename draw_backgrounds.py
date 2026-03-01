import datetime
import os
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

font_size = 20
font_size_large = 45
v_pad = 5 # num of pixels between each arrivals box
h_pad = 15 # num of pixels between the sides

train_to_colors = {
    "Blue": (0, 157, 220),
    "Red": (227, 25, 55)
}

ui_dir = "./ui"

class Display:
    def __init__(self) -> None:
        self.width = 640
        self.height = 400

        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = 2
        self.BLUE = 3
        self.RED = 4
        self.YELLOW = 5
        self.ORANGE = 6
        self.CLEAN = 7

inky_display = Display()
image = Image.new("RGB", (inky_display.width, inky_display.height), inky_display.BLACK)

arrivals_offset = v_pad * 2 + font_size

# Fonts
fnt_small = ImageFont.truetype("./fonts/FreeSans.otf", size=font_size)
fnt_large = ImageFont.truetype("./fonts/FreeSansBold.otf", size=font_size_large)

# Functions
def get_current_time() -> str:
    current_time = datetime.datetime.today()
    return current_time.strftime("%Y/%m/%d %H:%M:%S")

def create_arrivals_background(arrivals_data: pd.DataFrame, image: Image) -> Image:
    draw = ImageDraw.Draw(image)

    n_arrivals = arrivals_data.shape[0]
    arrival_box_height = ((inky_display.height - arrivals_offset) - (n_arrivals * v_pad)) / n_arrivals
    arrival_box_x1 = h_pad
    arrival_box_x2 = inky_display.width - h_pad

    # Draw each rectangle
    for i, row in arrivals_data.iterrows():

        i_arrival_box_y1 = arrivals_offset + ((arrival_box_height + v_pad) * i)
        i_arrival_box_y2 = i_arrival_box_y1 + arrival_box_height

        draw.rectangle(
            (
                arrival_box_x1, i_arrival_box_y1, 
                arrival_box_x2, i_arrival_box_y2
            ), 
            fill=train_to_colors[row["rt"]]
        )

        min_text_width = 25

        # Write arrivals text
        draw.text(
            (arrival_box_x1 + h_pad, (i_arrival_box_y1 + i_arrival_box_y2) / 2),
            row["destNm"],
            inky_display.WHITE,
            font=fnt_large
        )
        draw.text(
            (arrival_box_x2 - h_pad - min_text_width, (i_arrival_box_y1 + i_arrival_box_y2) / 2),
            str(round(row["tTArr"])),
            inky_display.WHITE,
            font=fnt_large
        )


    draw.text((h_pad, v_pad), f"Last Updated: {get_current_time()}", inky_display.WHITE, font=fnt_small)

    return image

"""
Given the coordinates of a box, align text within the box.

Params:
    xy: box coordinates of the form [(x0, y0), (x1, y1)]
    v_align: vertical alignment by relative position within the box. 0.5 corresponds to center
    v_align: horizontal alignment by relative position within the box. 0.5 corresponds to center
"""
def add_text_to_box(xy: list[tuple], v_align: float=0.5, h_align: float=0.5, align: str="left") -> None:
    pass


"""
Given desired coordinates and alignment, return aligned coordinates
"""
def align_text(xy: list[tuple], text: str, font: ImageFont.FreeTypeFont, h_align: float=0.5, v_align: float=0.5, align: str="left") -> list[tuple]:
    x, y = xy
    box_left, box_top, box_right, box_bottom = font.getbbox(text)

    text_height = box_bottom - box_top

    print(text_height)

    y_offset = text_height * v_align

    if align == "left":
        return (x, y - y_offset)
    if align == "right":
        return (x - box_right, y - y_offset)

"""
Adds coordinates at key parts of the image for debugging purposes.
"""
def add_grid_coord(image: Image, color=inky_display.WHITE) -> Image:
    draw = ImageDraw.Draw(image)

    # draw.text((0, 50), "(0, 50)", color, font=fnt_small)
    # draw.text((50, 50), "(50, 50)", color, font=fnt_small)
    # draw.text((0, 200), "(0, 200)", color, font=fnt_small)
    # draw.text((0, 250), "(0, 250)", color, font=fnt_small)
    # draw.text((0, 300), "(0, 300)", color, font=fnt_small)

    draw.line(((0, 50), (inky_display.width, 50)))
    draw.line(((50, 0), (50, inky_display.height)))

    new_align = align_text((50,50), "Hello", fnt_large, align="right")
    print(new_align)

    # draw.text((50,50), "Hello", color="red", font=fnt_small)
    draw.text(new_align, "Hello", color="blue", font=fnt_large)

    return image

"""
Save the image out. This is because Inky Impressions renders it better as a PNG than PIL image.
"""
def save_image(image: Image, out_path: str) -> None:
    image.save(out_path, "PNG")

if __name__ == "__main__":
    arrivals_data1 = pd.DataFrame({
        "staId": [40470],
        "staNm": ["Racine"],
        "rt": ["Blue"],
        "destNm": ["O'Hare"],
        "tTArr": [7.0],
        "isApp": [0],
        "isSch": [0],
        "isDly": [0],
        "idFlt": [0]
    })
    arrivals_data2 = pd.DataFrame({
        "staId": [40470, 40470],
        "staNm": ["Racine", "Racine"],
        "rt": ["Blue", "Red"],
        "destNm": ["O'Hare", "O'Hare"],
        "tTArr": [7.0, 5.0],
        "isApp": [0, 0],
        "isSch": [0, 0],
        "isDly": [0, 0],
        "idFlt": [0, 0]
    })
    arrivals_data3 = pd.DataFrame({
        "staId": [40470, 40470, 40470],
        "staNm": ["Racine", "Racine", "Racine"],
        "rt": ["Blue", "Blue", "Blue"],
        "destNm": ["O'Hare", "O'Hare", "Forest Park"],
        "tTArr": [7.0, 5.0, 15.0],
        "isApp": [0, 0, 0],
        "isSch": [0, 0, 0],
        "isDly": [0, 0, 0],
        "idFlt": [0, 0, 0]
    })
    arrivals_data4 = pd.DataFrame({
        "staId": [40470, 40470, 40470, 40470],
        "staNm": ["Racine", "Racine", "Racine", "Racine"],
        "rt": ["Blue", "Blue", "Blue", "Blue"],
        "destNm": ["O'Hare", "O'Hare", "Forest Park", "Forest Park"],
        "tTArr": [7.0, 5.0, 15.0, 20.0],
        "isApp": [0, 0, 0, 0],
        "isSch": [0, 0, 0, 0],
        "isDly": [0, 0, 0, 0],
        "idFlt": [0, 0, 0, 0]
    })
    # image = create_arrivals_background(arrivals_data4, image)
    image = add_grid_coord(image)
    save_image(image, os.path.join(ui_dir, "./cta_ui.png"))
    image.show()
