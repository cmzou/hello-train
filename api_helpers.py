import xml.etree.ElementTree as ET
import pandas as pd

import requests
import getpass
import os

try:
    api_key = os.environ["CTA_API_KEY"]
except KeyError:
    api_key = getpass.getpass("API Key:")
    os.environ["CTA_API_KEY"] = api_key

def call_get_arrivals(map_id: int) -> dict:
    arrivals_url = "http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx"

    payload = {
        "mapid": map_id,
        "key": api_key,
        "outputType": "JSON"
    }

    resp = requests.get(arrivals_url, params=payload)

    return resp.json()

def parse_arrivals_xml(xml_resp: str) -> pd.DataFrame:
    tree = ET.parse(xml_resp)

    return

def get_arrivals(map_id: int) -> pd.DataFrame:
    arrivals_resp = call_get_arrivals(map_id)

    return pd.DataFrame(arrivals_resp["ctatt"]["eta"])


if __name__ == "__main__":
    print(get_arrivals(40470))
