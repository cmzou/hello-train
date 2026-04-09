import pandas as pd
from PIL import Image, ImageDraw, ImageFont

from config.app_settings import ui_dir
from util import util

font_size = 20
font_size_large = 70
v_pad = 5 # num of pixels between each arrivals box
h_pad = 15 # num of pixels between the sides

train_to_colors = {
    "Blue": (0, 157, 220),
    "Red": (227, 25, 55),
    "NA": (86, 90, 92)
}

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

arrivals_offset = v_pad * 2 + font_size

# Fonts
fnt_small = ImageFont.truetype("./fonts/FreeSans.otf", size=font_size)
font_large_path = "./fonts/FreeSansBold.otf"
fnt_large = ImageFont.truetype(font_large_path, size=font_size_large)

# Functions
def divide_vspace_rectangles(inky_display, num_rectangles: int) -> tuple[int, int, int, int]:
    arrival_box_x1 = h_pad
    arrival_box_x2 = inky_display.width - h_pad
    arrival_box_height = ((inky_display.height - arrivals_offset) - (num_rectangles * v_pad)) / num_rectangles
    arrival_box_width = arrival_box_x2 - arrival_box_x1

    return arrival_box_x1, arrival_box_x2, arrival_box_width, arrival_box_height

"""
Calculates the optimal font size that fits font_perc of the max_height
"""
def calc_font_sizes(text: str, font_path: str, max_height: int, font_perc: float) -> int:
    font_size = 1

    increment_font = ImageFont.truetype(font_path, font_size)
    while increment_font.getbbox(text)[3] < max_height * font_perc:
        # Iterate until the text size is just larger than the criteria
        font_size += 1
        increment_font = ImageFont.truetype(font_path, font_size)

    return font_size

"""
For each text in a given list of strings, truncate the text if it's longer than the given length

Params:
    text_list: list of strings to truncate
    font_path: path to the font to check the length of
    font_size: size of the font
    max_length: max length in pixels each string can be
    truncation_type: order of truncation until the text fits:
        length: simple truncation from the right; delete each character until the text fits
        vowel: delete each vowel from the right until the text fits
"""
def edit_for_overlaps(text_list: list[str], font_path: str, font_size: int, max_length: int) -> list[str]:
    fnt_object = ImageFont.truetype(font_path, size=font_size)
    for i in range(len(text_list)):
        initial_text = text_list[i]
        current_length = fnt_object.getbbox(initial_text)[2]
        while current_length > max_length:
            text = text_list[i]

            if len(text) <= 1:
                break
            current_length = fnt_object.getbbox(text)[2]
            if current_length > max_length:
                text_list[i] = text[0:-1]
    return text_list

def create_arrivals_background(inky_display, arrivals_data: pd.DataFrame, image: Image) -> Image:
    draw = ImageDraw.Draw(image)

    n_arrivals = arrivals_data.shape[0]

    if n_arrivals == 0:
        draw.text(
            (h_pad, v_pad),
            "No arrivals data.",
            WHITE,
            font=fnt_large
        )

        return image

    arrival_box_x1, arrival_box_x2, arrival_box_width, arrival_box_height = divide_vspace_rectangles(inky_display, n_arrivals)

    # Draw each rectangle
    for i, row in arrivals_data.iterrows():

        i_arrival_box_y1 = arrivals_offset + ((arrival_box_height + v_pad) * i)
        i_arrival_box_y2 = i_arrival_box_y1 + arrival_box_height

        if row["rt"] in train_to_colors:
            fill_color = train_to_colors[row["rt"]]
        else:
            fill_color = train_to_colors["NA"]

        draw.rectangle(
            (
                arrival_box_x1, i_arrival_box_y1, 
                arrival_box_x2, i_arrival_box_y2
            ), 
            fill=fill_color
        )

        min_text_width = fnt_small.getbbox("min")[2]
        min_text_height = fnt_small.getbbox("min")[3]

        arrival_destination_text = row["nmArr"]
        arrival_time_text = row["tTArr"]

        arrival_destination_text_list = arrival_destination_text.split("\n")

        # Parse for overlaps
        arrival_destination_text_list[1:] = edit_for_overlaps(arrival_destination_text_list[1:], font_large_path, font_size_large, arrival_box_width * 0.75)

        if len(arrival_destination_text_list) == 1:
            arrival_destination_text_top = ""
            arrival_destination_text_bottom = arrival_destination_text_list[0]
        else:
            arrival_destination_text_top = arrival_destination_text_list[0]
            arrival_destination_text_bottom = arrival_destination_text_list[1]

        # Write arrivals text
        top_text_align = align_text(
            (arrival_box_x1 + h_pad, i_arrival_box_y1 + v_pad),
            arrival_destination_text_bottom,
            fnt_small,
            v_align=0
        )
        new_dest_align = align_text(
            (arrival_box_x1 + h_pad, (i_arrival_box_y1 + i_arrival_box_y2) / 2),
            arrival_destination_text_bottom,
            fnt_large
        )
        new_arr_align = align_text(
            (arrival_box_x2 - h_pad - min_text_width, (i_arrival_box_y1 + i_arrival_box_y2) / 2),
            arrival_time_text,
            fnt_large,
            align="right"
        )

        draw.text(
            top_text_align,
            arrival_destination_text_top,
            WHITE,
            font=fnt_small
        )
        draw.text(
            new_dest_align,
            arrival_destination_text_bottom,
            WHITE,
            font=fnt_large
        )
        draw.text(
            new_arr_align,
            arrival_time_text,
            WHITE,
            font=fnt_large
        )
        draw.text(
            (
                new_arr_align[0] + fnt_large.getbbox(arrival_time_text)[2] + (h_pad / 2),
                new_arr_align[1] + fnt_large.getbbox(arrival_time_text)[3] - min_text_height
            ),
            "min",
            WHITE,
            font=fnt_small
        )

    return image

def write_last_updated(image: Image):
    draw = ImageDraw.Draw(image)
    last_update_xy = (0, 0)

    draw.text(last_update_xy, f"Last Updated: {util.get_current_time()}", fill=BLACK, font=fnt_small)

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
