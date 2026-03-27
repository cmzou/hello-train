import os
import time
import datetime
import logging

from enum import Enum, auto

from display import draw_backgrounds, image_cycler
from data import data_parsers
from config import mode_settings

import gpiod
import gpiodevice
from gpiod.line import Bias, Direction, Edge

from threading import Thread, Event, Timer

from PIL import Image

from inky.auto import auto as inky_auto

logger = logging.getLogger(__name__)

inky_display = inky_auto(ask_user=True, verbose=True)

class DisplayMode(Enum):
    CTA = auto()
    CATS = auto()

current_mode = DisplayMode.CTA
current_route_i = 0

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
    exit.set()

def switch_to_cats():
    global current_mode
    current_mode = DisplayMode.CATS
    exit.set()

def handle_button(event):
    index = OFFSETS.index(event.line_offset)
    gpio_number = BUTTONS[index]
    label = LABELS[index]
    logger.info(f"Button press detected on GPIO #{gpio_number} label: {label}")

    if label == "A":
        switch_to_cta()
    if label == "B":
        switch_to_cats()

    # Mode specific actions
    if label == "D":
        if current_mode == DisplayMode.CTA:
            global current_route_i
            current_route_i = get_next_i_in_list()

def button_thread():
    while True:
        for event in request.read_edge_events():
            handle_button(event)

def switch_based_on_current_mode():
    if current_mode == DisplayMode.CTA:
        switch_to_cats()
    else:
        switch_to_cta()

"""
Returns the next valid index sequentially in a list
"""
def get_next_i_in_list(current_i: int, ls: list):
    if current_i + 1 >= len(ls):
        current_i = 0
    else:
        current_i += 1
    return current_i

def scheduler():
    while True:
        interval_begin = mode_settings.scheduled_intervals[0][0]
        interval_end = mode_settings.scheduled_intervals[0][1]

        seconds_until_begin = image_cycler.calc_time_until_refresh(interval_begin)
        seconds_until_end = image_cycler.calc_time_until_refresh(interval_end)

        seconds_until_refresh = min(seconds_until_begin, seconds_until_end)

        time.sleep(seconds_until_refresh)

        switch_based_on_current_mode()

Thread(target=button_thread, daemon=True).start()

def setup():
    image_cycler.setup()

    Thread(target=scheduler, daemon=True).start()

def main():
    setup()

    while True:
        match current_mode:
            case DisplayMode.CTA:
                exit.clear()
                # The image cycling time is non-negligible -- will eventually compound and stop refreshing with same interval each time
                current_time = datetime.datetime.now()
                next_refresh_time = current_time + datetime.timedelta(seconds=mode_settings.cta_refresh_seconds)
                next_refresh_time = next_refresh_time.strftime("%I:%M %p")

                current_route = mode_settings.display_routes[current_route_i]
                arrivals_data = data_parsers.get_and_parse_data(data_parsers.route_to_ids[current_route]["id"], data_parsers.route_to_ids[current_route]["transport_mode"])
                image = Image.new("RGB", (inky_display.width, inky_display.height), draw_backgrounds.BLACK)
                image = draw_backgrounds.create_arrivals_background(inky_display, arrivals_data, image)
                draw_backgrounds.save_image(image, os.path.join(draw_backgrounds.ui_dir, "./cta_ui.png"))
                image_cycler.displays["cta"].set_current_image()
                image_cycler.displays["cta"].display_current_image(inky_display, last_update_color=draw_backgrounds.WHITE, last_update_fnt=draw_backgrounds.fnt_small)
                exit.wait(image_cycler.calc_time_until_refresh(next_refresh_time))

            case DisplayMode.CATS:
                exit.clear()
                image_cycler.displays["cat"].set_current_image()
                image_cycler.displays["cat"].display_current_image(inky_display, last_update_color=draw_backgrounds.BLACK)
                if mode_settings.enable_scheduled_shuffle:
                    seconds_until_refresh = image_cycler.calc_time_until_refresh(mode_settings.scheduled_refresh_time)
                else:
                    seconds_until_refresh = mode_settings.shuffle_seconds
                exit.wait(seconds_until_refresh)
