import pandas as pd
import datetime
import logging

from data import get_data
from config import mode_settings, app_settings

logger = logging.getLogger(__name__)

"""
The format of this dict is:
{
    <user friendly name of stop>: {
        "transport_mode": train|bus,
        "id": stpid|staId,
        "route_name": <user friendly name of bus>
    }
}
"""
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
        arrivals_data["nmArr"] = "#" + arrivals_data["rt"] + " " + arrivals_data["stpnm"].str[0:5] + " " + arrivals_data["rtdir"] + " to \n" + arrivals_data["des"]

"""
Calculate the time remaining from the arrival time and current time
Modifies the dataframe in place and adds a new column "tTArr" (time 'till arrival) in minutes
"""
def calc_time_remaining(arrivals_data: pd.DataFrame, transport_mode: str) -> None:
    if transport_mode == "train":
        current_time = datetime.datetime.now()
        arrivals_data["tTArr"] = arrivals_data["arrT"] - current_time
        arrivals_data["tTArr"] = arrivals_data["tTArr"].apply(lambda x: x.total_seconds())
        arrivals_data["tTArr"] = arrivals_data["tTArr"] / 60
        arrivals_data["tTArr"] = arrivals_data["tTArr"].round().astype(int)
        arrivals_data["tTArr"] = arrivals_data["tTArr"].astype(str)
        arrivals_data.loc[arrivals_data["isApp"] == 1, "tTArr"] = "0"
    elif transport_mode == "bus":
        arrivals_data["tTArr"] = arrivals_data["prdctdn"]
        arrivals_data.loc[arrivals_data["tTArr"] == "DUE", "tTArr"] = "0"

    arrivals_data.drop(arrivals_data[(arrivals_data["tTArr"].astype(int) < mode_settings.min_arrival_to_omit)].index, inplace=True)
    arrivals_data.loc[arrivals_data["tTArr"] == 0, "tTArr"] = "DUE"
    arrivals_data.reset_index(drop=True, inplace=True)

"""
Given a route ID and type, get the data

Return:
    None if the internet is suspected to be down
"""
def get_and_parse_data(route_id: str, transport_mode: str) -> pd.DataFrame:
    if transport_mode == "train":
        arrivals_data = get_data.get_train_arrivals(route_id)
    elif transport_mode == "bus":
        arrivals_data = get_data.get_bus_arrivals(route_id)
    else:
        raise ValueError(f"Invalid transport_mode given: {transport_mode}")

    if arrivals_data is None:
        return None

    if arrivals_data.shape[0] != 0:
        parse_data(arrivals_data, transport_mode)
        calc_time_remaining(arrivals_data, transport_mode)

        arrivals_data = arrivals_data.iloc[0:app_settings.max_results_returned]

    return arrivals_data

"""
Given a route name and type, search for the data
"""
def search_data(transport_mode: str, route_name: str) -> None:
    pass
