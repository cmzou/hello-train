import pandas as pd

import requests
import time
import logging

from config import secrets, app_settings

logger = logging.getLogger(__name__)

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
            logger.warning(f"Requests timed out, sleeping {i} out of {app_settings.max_retries}...")
            time.sleep(5)
        except requests.HTTPError as e:
            if 500 <= e.response.status_code < 600:  # Server error - retry
                logger.warning(f"Train arrivals error, sleeping {i} out of {app_settings.max_retries}...")
                time.sleep(5)
            else:
                raise e

    return {}

def get_train_arrivals(map_id: int) -> pd.DataFrame:
    try:
        arrivals_resp = call_get_train_arrivals(map_id)

        return pd.DataFrame(arrivals_resp["ctatt"]["eta"])
    except requests.ConnectionError:
        # Likely no internet
        logger.error(f"Train arrivals endpoint failed with ConnectionError")
        return None
    except (requests.RequestException, KeyError, ValueError) as e:
        logger.error(f"Train arrivals endpoint failed with error: {e}")
        return None

def call_get_bus_arrivals(stp_id: int) -> dict:
    arrivals_url = "https://www.ctabustracker.com/bustime/api/v3/getpredictions"

    payload = {
        "stpid": stp_id,
        "key": secrets.secrets.config["API"]["BUS_API_KEY"],
        "format": "json",
        "top": app_settings.max_results_returned*2
    }

    for i in range(app_settings.max_retries):
        try:
            resp = requests.get(arrivals_url, params=payload)
            resp.raise_for_status()
            return resp.json()
        except requests.Timeout as e:
            logger.warning(f"Requests timed out, sleeping {i} out of {app_settings.max_retries}...")
            time.sleep(5)
        except requests.HTTPError as e:
            if 500 <= e.response.status_code < 600:  # Server error - retry
                logger.warning(f"Server error, sleeping {i} out of {app_settings.max_retries}...")
                time.sleep(5)
            else:
                raise e

    return {}

def get_bus_arrivals(stp_id: int) -> pd.DataFrame:
    try:
        arrivals_resp = call_get_bus_arrivals(stp_id)

        return pd.DataFrame(arrivals_resp["bustime-response"]["prd"])
    except requests.ConnectionError:
        # Likely no internet
        logger.error(f"Bus arrivals endpoint failed with ConnectionError")
        return None
    except (requests.RequestException, KeyError, ValueError) as e:
        logger.error(f"Bus arrivals endpoint failed with error: {e}")
        return None

"""
Get and save necessary bus route data for querying and display
"""
def call_get_bus_routes() -> dict:
    routes_url = "https://www.ctabustracker.com/bustime/api/v3/getroutes"

    payload = {
        "key": secrets.secrets.config["API"]["BUS_API_KEY"],
        "format": "json",
    }

    for i in range(app_settings.max_retries):
        try:
            resp = requests.get(routes_url, params=payload)
            resp.raise_for_status()
            return resp.json()
        except requests.Timeout:
            logger.warning(f"Requests timed out, sleeping {i} out of {app_settings.max_retries}...")
            time.sleep(5)
        except requests.HTTPError as e:
            if 500 <= e.response.status_code < 600:  # Server error - retry
                logger.warning(f"Bus routes server error, sleeping {i} out of {app_settings.max_retries}...")
                time.sleep(5)
            else:
                raise e

    return {}

def get_bus_routes() -> pd.DataFrame:
    try:
        routes_data = call_get_bus_routes()
        routes_df = pd.DataFrame(routes_data["bustime-response"]["routes"])
        routes_df.to_csv("./data/routes.csv", index=False)
    except (requests.RequestException, KeyError, ValueError) as e:
        # Use old data
        logger.error(f"Bus routes endpoint failed with error: {e}")
        routes_df = pd.read_csv("./data/routes.csv", index=False)

    return routes_df

def get_bus_stops(route_id: int) -> dict:
    pass

def search_call_get_bus_data(search_str: str, routes_df: pd.DataFrame) -> None:
    search_results = routes_df[routes_df["rtnm"].str.lower().str.contains(search_str.lower)]

    try:
        # Find stop id by name
        stops_df = get_bus_stops()
    except:
        pass


    stops_url = "https://www.ctabustracker.com/bustime/api/v3/getstops"
    directions_url = "https://www.ctabustracker.com/bustime/api/v3/getdirections"

    try:
        # Find stop id by name
        directions_data = requests.get(directions_url, params={**payload, "rt": route_id})
        stops_data = requests.get(stops_url, params={**payload, "rt": route_id, "dir": direction})

    except:
        pass
