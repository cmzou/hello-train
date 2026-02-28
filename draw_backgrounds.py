import datetime
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

font_size = 13
font_size_large = 20
v_pad = 5 # num of pixels between each arrivals box
h_pad = 15 # num of pixels between the sides

train_to_colors = {
    "Blue": (0, 157, 220),
    "Red": (227, 25, 55)
}

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
image = Image.new("P", (inky_display.width, inky_display.height), inky_display.BLACK)

arrivals_offset = inky_display.height / 2

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


    draw.text((0, 0), f"Last Updated: {get_current_time()}", inky_display.WHITE, font=fnt_small)

    return image

"""
Adds coordinates at key parts of the image for debugging purposes.
"""
def add_grid_coord(image: Image, color=inky_display.WHITE) -> Image:
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
    image = create_arrivals_background(arrivals_data3, image)
    save_image(image, "./current_background.png")
    image.show()
