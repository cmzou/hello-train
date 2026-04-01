import pandas as pd

import requests
import time

from config import secrets, app_settings

def call_get_train_arrivals(map_id: int) -> dict:
    arrivals_url = "http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx"

    payload = {
        "mapid": map_id,
        "key": secrets.secrets.config["API"]["CTA_API_KEY"],
        "outputType": "JSON",
        "max": app_settings.max_results_returned*2
    }


    for i in range(app_settings.max_retries):
        try:
            resp = requests.get(arrivals_url, params=payload)
            resp.raise_for_status()
            return resp.json()
        except requests.Timeout as e:
            time.sleep(5)
        except requests.HTTPError as e:
            if 500 <= e.response.status_code < 600:  # Server error - retry
                time.sleep(5)
            else:
                raise e

    return {}

def get_train_arrivals(map_id: int) -> pd.DataFrame:
    try:
        arrivals_resp = call_get_train_arrivals(map_id)

        return pd.DataFrame(arrivals_resp["ctatt"]["eta"])
    except (requests.RequestException, KeyError, ValueError):
        return pd.DataFrame()

def call_get_bus_arrivals(stp_id: int) -> dict:
    arrivals_url = "https://www.ctabustracker.com/bustime/api/v3/getpredictions"

    payload = {
        "stpid": stp_id,
        "key": secrets.secrets.config["API"]["BUS_API_KEY"],
        "format": "json",
        "top": app_settings.max_results_returned*2
    }

    resp = requests.get(arrivals_url, params=payload)

    return resp.json()

def get_bus_arrivals(stp_id: int) -> pd.DataFrame:
    arrivals_resp = call_get_bus_arrivals(stp_id)

    return pd.DataFrame(arrivals_resp["bustime-response"]["prd"])
