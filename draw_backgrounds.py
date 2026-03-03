import datetime
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

font_size = 20
font_size_large = 70
v_pad = 5 # num of pixels between each arrivals box
h_pad = 15 # num of pixels between the sides

train_to_colors = {
    "Blue": (0, 157, 220),
    "Red": (227, 25, 55)
}

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

ui_dir = "./ui"

arrivals_offset = v_pad * 2 + font_size

# Fonts
fnt_small = ImageFont.truetype("./fonts/FreeSans.otf", size=font_size)
fnt_large = ImageFont.truetype("./fonts/FreeSansBold.otf", size=font_size_large)

# Functions
def get_current_time() -> str:
    current_time = datetime.datetime.today()
    return current_time.strftime("%Y/%m/%d %H:%M:%S")

def create_arrivals_background(inky_display, arrivals_data: pd.DataFrame, image: Image) -> Image:
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

        min_text_width = fnt_small.getbbox("min")[2]
        min_text_height = fnt_small.getbbox("min")[3]

        # Write arrivals text
        new_dest_align = align_text(
            (arrival_box_x1 + h_pad, (i_arrival_box_y1 + i_arrival_box_y2) / 2),
            row["destNm"],
            fnt_large
        )
        new_arr_align = align_text(
            (arrival_box_x2 - h_pad - min_text_width, (i_arrival_box_y1 + i_arrival_box_y2) / 2),
            str(round(row["tTArr"])),
            fnt_large,
            align="right"
        )

        draw.text(
            new_dest_align,
            row["destNm"],
            WHITE,
            font=fnt_large
        )
        draw.text(
            new_arr_align,
            str(round(row["tTArr"])),
            WHITE,
            font=fnt_large
        )
        draw.text(
            (
                new_arr_align[0] + fnt_large.getbbox(str(round(row["tTArr"])))[2] + (h_pad / 2),
                new_arr_align[1] + fnt_large.getbbox(str(round(row["tTArr"])))[3] - min_text_height
            ),
            "min",
            WHITE,
            font=fnt_small
        )


    # draw.text((h_pad, v_pad), f"Last Updated: {get_current_time()}", inky_display.WHITE, font=fnt_small)

    return image

"""
Given desired coordinates and alignment, return aligned coordinates
"""
def align_text(xy: list[tuple], text: str, font: ImageFont.FreeTypeFont, h_align: float=0.5, v_align: float=0.5, align: str="left") -> list[tuple]:
    x, y = xy
    _, _, text_length, text_height = font.getbbox(text)

    y_offset = text_height * v_align

    if align == "left":
        return (x, y - y_offset)
    if align == "right":
        return (x - text_length, y - y_offset)

"""
Adds coordinates at key parts of the image for debugging purposes.
"""
def add_grid_coord(image: Image, color) -> Image:
    draw = ImageDraw.Draw(image)

    draw.text((0, 50), "(0, 50)", color, font=fnt_small)
    draw.text((50, 50), "(50, 50)", color, font=fnt_small)
    draw.text((0, 200), "(0, 200)", color, font=fnt_small)
    draw.text((0, 250), "(0, 250)", color, font=fnt_small)
    draw.text((0, 300), "(0, 300)", color, font=fnt_small)

    return image

"""
Save the image out. This is because Inky Impressions renders it better as a PNG than PIL image.
"""
def save_image(image: Image, out_path: str) -> None:
    image.save(out_path, "PNG")

