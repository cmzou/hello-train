import pandas as pd

import requests
import settings

max_results_returned = 10

def call_get_train_arrivals(map_id: int) -> dict:
    arrivals_url = "http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx"

    payload = {
        "mapid": map_id,
        "key": settings.settings.config["API"]["CTA_API_KEY"],
        "outputType": "JSON",
        "max": max_results_returned
    }

    resp = requests.get(arrivals_url, params=payload)

    return resp.json()

def get_train_arrivals(map_id: int) -> pd.DataFrame:
    arrivals_resp = call_get_train_arrivals(map_id)

    return pd.DataFrame(arrivals_resp["ctatt"]["eta"])
