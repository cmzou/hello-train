import pandas as pd
import datetime

from data import get_data
from config import mode_settings

route_to_ids = {
    "Racine": {
        "transport_mode": "train",
        "id": 40470
    },
    "Ashland & Van Buren": {
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


def parse_data(arrivals_data: pd.DataFrame, transport_mode) -> None:
    if transport_mode == "train":
        arrivals_data["arrT"] = pd.to_datetime(arrivals_data["arrT"])
        arrivals_data["nmArr"] = arrivals_data["destNm"]
    elif transport_mode == "bus":
        arrivals_data["nmArr"] = arrivals_data["rtdir"] + " to \n" + arrivals_data["des"]

"""
Calculate the time remaining from the arrival time and current time
Modifies the dataframe in place and adds a new column "tTArr" (time 'till arrival) in minutes
"""
def calc_time_remaining(arrivals_data: pd.DataFrame, transport_mode: str) -> None:
    if transport_mode == "train":
        arrivals_data["tTArr"] = arrivals_data["arrT"] - datetime.datetime.now()
        arrivals_data["tTArr"] = arrivals_data["tTArr"].apply(lambda x: x.total_seconds())
        arrivals_data["tTArr"] = arrivals_data["tTArr"] / 60
        arrivals_data["tTArr"] = arrivals_data["tTArr"].round().astype(int)
        arrivals_data["tTArr"] = arrivals_data["tTArr"].astype(str)
        arrivals_data.loc[arrivals_data["isApp"] == 1, 'tTArr'] = "DUE"
    elif transport_mode == "bus":
        arrivals_data["tTArr"] = arrivals_data["prdctdn"]

    arrivals_data.drop(arrivals_data[arrivals_data["tTArr"].astype(int) < mode_settings.min_arrival_to_omit].index, inplace=True)
    arrivals_data.reset_index(drop=True, inplace=True)

"""
Given a route ID and type, get the data
"""
def get_and_parse_data(route_id: str, transport_mode: str) -> None:
    if transport_mode == "train":
        arrivals_data = get_data.get_train_arrivals(route_id)
    elif transport_mode == "bus":
        arrivals_data = get_data.get_bus_arrivals(route_id)
    else:
        raise ValueError(f"Invalid transport_mode give: {transport_mode}")

    parse_data(arrivals_data, transport_mode)
    calc_time_remaining(arrivals_data, transport_mode)

    return arrivals_data
