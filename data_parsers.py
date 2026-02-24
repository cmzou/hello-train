import pandas as pd
import datetime

import api_helpers

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

"""
Given a dictionary of station information to get,
add new data to the dictionary
"""
def get_and_parse_data(station_data: dict) -> None:
    for i in range(len(station_data["staNm"])):
        arrivals_data = api_helpers.get_train_arrivals(station_data["staId"][i])
        parse_data(arrivals_data)
        calc_time_remaining(arrivals_data)

        station_data["staData"].append(arrivals_data)
