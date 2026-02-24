import pandas as pd
import datetime

import api_helpers

station_data = {
    "staNm": ["Racine"],
    "staId": [40470],
    "staData": []
}

def parse_data(arrivals_data: pd.DataFrame) -> None:
    arrivals_data["arrT"] = pd.to_datetime(arrivals_data["arrT"])

"""
Calculate the time remaining from the arrival time and current time
Modifies the dataframe in place and adds a new column "tTArr" (time 'till arrival) in minutes
"""
def calc_time_remaining(arrivals_data: pd.DataFrame) -> None:
    arrivals_data["tTArr"] = arrivals_data["arrT"] - datetime.datetime.now()
    arrivals_data["tTArr"] = arrivals_data["tTArr"].apply(lambda x: x.total_seconds())
    arrivals_data["tTArr"] = arrivals_data["tTArr"] / 60
    arrivals_data["tTArr"] = arrivals_data["tTArr"].round()

def get_and_parse_data() -> None:
    for i in range(len(station_data["staNm"])):
        arrivals_data = api_helpers.get_arrivals(station_data["staId"][i])
        parse_data(arrivals_data)
        calc_time_remaining(arrivals_data)

        station_data["staData"].append(arrivals_data)
