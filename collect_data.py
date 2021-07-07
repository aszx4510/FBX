import json
from pprint import pprint

import pandas as pd
import requests
from IPython.display import display

overview_url = 'https://fbx.freightos.com/api/ticker'
lanes_url = 'https://fbx.freightos.com/locales/en/lanes.json'
url_template = 'https://fbx.freightos.com/api/lane/{lane}?isDaily=false'

chinese_names = {
    'FBX': '全球貨運指數',
    'FBX01': '中國-美西 去程',
    'FBX02': '中國-美西 回程',
    'FBX03': '中國-美東 去程',
    'FBX04': '中國-美東 回程',
    'FBX11': '中國-北歐 去程',
    'FBX12': '中國-北歐 回程',
    'FBX13': '中國-地中海 去程',
    'FBX14': '中國-地中海 回程',
    'FBX21': '美東-北歐 去程',
    'FBX22': '美東-北歐 回程',
    'FBX24': '歐洲-拉美東岸',
    'FBX26': '歐洲-拉美西岸',
}


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


def all_fbx(fbx_lanes):

    df_list = []

    for lane, lane_name in fbx_lanes.items():

        print(lane, lane_name)

        data = query_data(url_template.format(lane=lane))

        df_fbx = pd.DataFrame(data['indexPoints'])
        df_fbx = df_fbx[['indexDate', 'value']].rename(columns={'value': lane}).round(2).set_index('indexDate')

        df_list.append(df_fbx)

    df_all_fbx = pd.concat(df_list, axis='columns').rename(columns=chinese_names)

    display(df_all_fbx)

    df_all_fbx.to_csv('all_fbx.csv')


if __name__ == '__main__':

    lanes = get_lanes()

    print(lanes)

    # Export all fbx data
    all_fbx(lanes)
