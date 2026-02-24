import pandas as pd

import requests
import yaml

class Config:
    def __init__(self) -> None:
        self.config = yaml.safe_load(open("./config.yml"))

config = Config()

def call_get_arrivals(map_id: int) -> dict:
    arrivals_url = "http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx"

    payload = {
        "mapid": map_id,
        "key": config.config["API"]["CTA_API_KEY"],
        "outputType": "JSON"
    }

    resp = requests.get(arrivals_url, params=payload)

    return resp.json()

def get_arrivals(map_id: int) -> pd.DataFrame:
    arrivals_resp = call_get_arrivals(map_id)

    return pd.DataFrame(arrivals_resp["ctatt"]["eta"])


if __name__ == "__main__":
    print(get_arrivals(40470))
