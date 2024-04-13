import requests
from json_excel_converter import Converter
from json_excel_converter.xlsx import Writer

endpoint = 'http://budget.gov.ru/epbs/registry/7710568760-repexecutincome/data'

reg_list = ["01", "02", "03", "04", "05", "06", "07", "08", "09"]
for i in range(10, 85):
    reg_list.append(str(i))

data = []

for i in reg_list:
    print(i, "Start")
    query_params = {"filterperiod": "01012019", "filterperiodicity": "Y", "pageSize": "10000", "filteroktmo.regioncode": i, "filterblocks.info": "PERKB", "FORMCODEOKUD": "0503317", "filterkd.code": ["00000000000000000", "10000000000000000", "20000000000000000"]}
    resp = requests.get(endpoint, params=query_params)

    if resp.status_code == 200:
        data.append(resp.json()['data'])
    else:
        print(resp.status_code)
    print(i, "Done")

print("Excel write Start")
conv = Converter()
conv.convert(data, Writer(file=f'output.xlsx'))
print("Excel write Done")
