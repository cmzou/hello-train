import pandas as pd

import requests
from config import secrets

max_results_returned = 4
max_retries = 3

def call_get_train_arrivals(map_id: int) -> dict:
    arrivals_url = "http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx"

    payload = {
        "mapid": map_id,
        "key": secrets.secrets.config["API"]["CTA_API_KEY"],
        "outputType": "JSON",
        "max": max_results_returned
    }

    resp = requests.get(arrivals_url, params=payload)

    return resp.json()

def get_train_arrivals(map_id: int) -> pd.DataFrame:
    arrivals_resp = call_get_train_arrivals(map_id)

    return pd.DataFrame(arrivals_resp["ctatt"]["eta"])

def call_get_bus_arrivals(stp_id: int) -> dict:
    arrivals_url = "https://www.ctabustracker.com/bustime/api/v3/getpredictions"

    payload = {
        "stpid": stp_id,
        "key": secrets.secrets.config["API"]["BUS_API_KEY"],
        "format": "json",
        "top": max_results_returned
    }

    resp = requests.get(arrivals_url, params=payload)

    return resp.json()

def get_bus_arrivals(stp_id: int) -> pd.DataFrame:
    arrivals_resp = call_get_bus_arrivals(stp_id)

    return pd.DataFrame(arrivals_resp["bustime-response"]["prd"])
