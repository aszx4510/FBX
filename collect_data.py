import json

import pandas as pd
import requests
from IPython.display import display

overview_url = 'https://fbx.freightos.com/api/ticker'
lanes_url = 'https://fbx.freightos.com/locales/en/lanes.json'
url_template = 'https://fbx.freightos.com/api/lane/{lane}?isDaily=false'


def query_data(url):

    r = requests.get(url)
    if r.status_code != 200:
        raise ValueError(f'Status code of response should be [200 OK], but it is {r.status_code}')

    return json.loads(r.text)


def get_lanes():

    lanes_data = query_data(lanes_url)

    # Remove noise data
    lanes_data = {k: v for k, v in lanes_data.items() if k.startswith('FBX')}

    return lanes_data


def all_fbx(lanes):
    pass


if __name__ == '__main__':
    df_lanes = get_lanes()

    display(df_lanes)

