import requests
from json_excel_converter import Converter 
from json_excel_converter.xlsx import Writer

endpoint = 'http://budget.gov.ru/epbs/registry/7710568760-repexecutincome/data'
query_params = {"filterperiod": "01012019", "filterperiodicity": "Y", "pageSize": "10000", "filteroktmo.oktmoname": "Новосибирская область", "blocks": "PERKB", "FORMCODEOKUD": "0503317"}
resp = requests.get(endpoint, params=query_params)

conv = Converter()
print(type(resp.json()))
conv.convert(resp.json()['data'], Writer(file='output.xlsx'))
