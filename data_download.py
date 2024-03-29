import requests
import pandas as pd
from pandas import json_normalize


def data_load(url, params):
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(response.status_code)


'''
'https://budget.gov.ru/epbs/registry/7710568760-EXECUTBUDGET/data?filterperiod=01012019&filterperiodicity=Y&pageSize=100&filteroktmo.oktmoname=Новосибирская область&blocks=PERKB'
'''

endpoint = 'https://budget.gov.ru/epbs/registry/7710568760-EXECUTBUDGET/data'
query_params = {"filterperiod": "01012019", "filterperiodicity": "Y", "pageSize": "100", "filteroktmo.oktmoname": "Новосибирская область", "blocks": "PERKB", "FORMCODEOKUD": "0503317"}
#data = data_load(endpoint, query_params)
#print(data)

'''
def data_file_write(url, params, file_name):
    response = requests.get(url, params=params)
    if response.status_code == 200:
        with open(file_name, 'w', encoding="utf8") as f:
            f.write(response.text)
    else:
        print(response.status_code)


data_file_write(endpoint, query_params, 'data.json')
'''

resp = requests.get(endpoint, params=query_params)
df = json_normalize(resp.json())
df.to_excel('data_excel.xlsx')
