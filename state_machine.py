import os
import logging

from enum import Enum, auto

import image_cycler
import draw_backgrounds
import data_parsers

import gpiod
import gpiodevice
from gpiod.line import Bias, Direction, Edge

from threading import Event

from PIL import Image

from inky.auto import auto as inky_auto

logger = logging.getLogger(__name__)

inky_display = inky_auto(ask_user=True, verbose=True)

sleep_seconds = 60 * 5
ui_dir = "./ui"

class DisplayMode(Enum):
    CTA = auto()
    CATS = auto()
    SETTINGS = auto()

current_mode = DisplayMode.CTA

BUTTONS = [5, 6, 16, 24]
LABELS = ["A", "B", "C", "D"]

INPUT = gpiod.LineSettings(direction=Direction.INPUT, bias=Bias.PULL_UP, edge_detection=Edge.FALLING)

chip = gpiodevice.find_chip_by_platform()

OFFSETS = [chip.line_offset_from_id(id) for id in BUTTONS]
line_config = dict.fromkeys(OFFSETS, INPUT)

request = chip.request_lines(consumer="inky7-buttons", config=line_config)

exit = Event()

def switch_to_cta():
    global current_mode
    current_mode = DisplayMode.CTA

def switch_to_cats():
    global current_mode
    current_mode = DisplayMode.CATS

def handle_button(event):
    index = OFFSETS.index(event.line_offset)
    gpio_number = BUTTONS[index]
    label = LABELS[index]
    logger.info(f"Button press detected on GPIO #{gpio_number} label: {label}")

    if label == "A":
        switch_to_cta()
    if label == "B":
        switch_to_cats()

def setup():
    image_cycler.setup()

def main():
    setup()

    while True:
        for event in request.read_edge_events():
            exit.set()
            handle_button(event)
        match current_mode:
            case DisplayMode.CTA:
                arrivals_data = data_parsers.get_and_parse_data(data_parsers.route_to_ids["Racine"]["id"], data_parsers.route_to_ids["Racine"]["transport_mode"])
                image = Image.new("RGB", (inky_display.width, inky_display.height), draw_backgrounds.BLACK)
                image = draw_backgrounds.create_arrivals_background(inky_display, arrivals_data, image)
                draw_backgrounds.save_image(image, os.path.join(ui_dir, "./cta_ui.png"))
                image_cycler.displays["cta"].set_current_image()
                image_cycler.displays["cta"].display_current_image(inky_display, last_update_color=draw_backgrounds.WHITE, last_update_fnt=draw_backgrounds.fnt_small)
                if exit.wait(sleep_seconds):
                    exit.clear()

            case DisplayMode.CATS:
                image_cycler.displays["cat"].set_current_image()
                image_cycler.displays["cat"].display_current_image(inky_display)
                if exit.wait(sleep_seconds):
                    exit.clear()
