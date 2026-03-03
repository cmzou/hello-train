import pandas as pd
import datetime

import api_helpers

route_to_ids = {
    "Racine": {
        "transport_mode": "train",
        "id": 40470
    },
    "9": {
        "transport_mode": "bus",
        "id": 51
    }
}

transport_mode_to_id_name = {
    "train": "staId",
    "bus": "stpid"
}

route_to_colname = {
    "train": "staNm",
    "bus": "rtdd"
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

"""
Given a route ID and type, get the data
"""
def get_and_parse_data(route_id: str, transport_mode: str) -> None:
    if transport_mode == "train":
        arrivals_data = api_helpers.get_train_arrivals(route_id)
    elif transport_mode == "bus":
        arrivals_data = api_helpers.get_bus_arrivals(route_id)
    else:
        raise ValueError(f"Invalid transport_mode give: {transport_mode}")

    parse_data(arrivals_data)
    calc_time_remaining(arrivals_data)

    return arrivals_data
