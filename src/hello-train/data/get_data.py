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

def call_bus_route_directions(rt: str) -> dict:
    directions_url = "https://www.ctabustracker.com/bustime/api/v3/getdirections"

    payload = {
        "rt": rt,
        "key": secrets.secrets.config["API"]["BUS_API_KEY"],
        "format": "json",
    }

    resp = requests.get(directions_url, params=payload)
    resp.raise_for_status()
    return resp.json()

def get_bus_route_directions(rt: str) -> pd.DataFrame:
    directions_data = call_bus_route_directions(rt)
    directions_df = pd.DataFrame(directions_data["bustime-response"]["directions"])
    directions_df.to_csv(f"./data/directions_{rt}.csv", index=False)

    return directions_df

def call_bus_stops(rt: str, directions: list) -> dict:
    stops_url = "https://www.ctabustracker.com/bustime/api/v3/getstops"

    stops = {}

    for direction in directions:
        payload = {
            "rt": rt,
            "key": secrets.secrets.config["API"]["BUS_API_KEY"],
            "format": "json",
            "dir": direction
        }

        resp = requests.get(stops_url, params=payload)
        resp.raise_for_status()

        stops[direction] = resp.json()

    return stops

def get_bus_stops(rt: str, directions: list) -> pd.DataFrame:
    stops_data = call_bus_stops(rt, directions)
    # Add direction data to stops
    for d in stops_data:
        for i in range(len(stops_data[d]["bustime-response"]["stops"])):
            stops_data[d]["bustime-response"]["stops"][i]["dir"] = d

    stops_df = pd.concat([pd.DataFrame(stops_data[d]["bustime-response"]["stops"]) for d in stops_data])
    stops_df.to_csv(f"./data/stops_{rt}.csv", index=False)

    return stops_df

"""
Searches for bi-directional bus stop data given a search string. Defaults to searching via name.

Params:
    search_type: whether to search by route name or by route ID; acceptable values: name, id
    exact_match: bool, whether to search for exact matches or not. if not exact match, will error on multiple returns
"""
def search_call_get_bus_stop_data(search_str: str, search_type: str="name", exact_match: bool=False) -> None:
    routes_df = get_bus_routes()

    if search_type == "name":
        search_col = "rtnm"
    elif search_type == "id":
        search_col = "rt"
    else:
        raise ValueError(f"Invalid search type given: {search_type}")

    if exact_match:
        search_results = routes_df[routes_df[search_col].str.lower() == search_str.lower()]
    else:
        search_results = routes_df[routes_df[search_col].str.lower().str.contains(search_str.lower())]

    if search_results.shape[0] > 1 : # multiple results returned
        logger.warning(f"Multiple routes returned:\n{search_results}")
        raise ValueError("Multiple routes found. Edit the route name and try again.")
    elif search_results.shape[0] == 0:
        logger.error("No routes found.")
        raise ValueError("No routes found. Edit the route name and try again.")

    rt = search_results.iloc[0]["rt"]

    # Get available directions
    directions = get_bus_route_directions(rt)["id"].to_list()
    # Get all bi-directional stops
    stops_df = get_bus_stops(rt, directions)

    stops_df["search_type"] = search_type
    stops_df["exact_match"] = exact_match
    stops_df["rt"] = rt

    return stops_df
