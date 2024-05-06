import requests
import json

endpoint = 'http://budget.gov.ru/epbs/registry/7710568760-repexecutincome/data'

reg_list = [f'{i:02d}' for i in range(1, 85)]

data = []
query_params = {"filterperiod": "01012019", "filterperiodicity": "Y", "pageSize": "10000", "filteroktmo.regioncode": None, "filterblocks.info": "perkb", 
                "filterFormcode.formcodeokud": "0503317", "filterkd.code": ["00000000000000000", "10000000000000000", "20000000000000000"]}

for i in reg_list:
    print(i, "Start")
    query_params["filteroktmo.regioncode"] = i
    resp = requests.get(endpoint, params=query_params)
        
    if resp.status_code == 200:
        data.append(resp.json())
    else:
        print(resp.status_code)
    print(i, "Done")

with open('data2.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
