import requests


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
data = data_load(endpoint, query_params)
print(data)
