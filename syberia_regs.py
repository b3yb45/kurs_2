import requests
import json
import datetime
from dateutil.relativedelta import relativedelta

END_YEAR = 2024
END_MONTH = 1

endpoint = 'http://budget.gov.ru/epbs/registry/7710568760-repexecutincome/data'

reg_list = ['Республика Алтай', 'Республика Тыва', 'Республика Хакасия', 'Алтайский край', 'Красноярский край', 'Иркутская область', 'Кемеровская область - Кузбасс', 'Новосибирская область', 'Омская область', 'Томская область', 'Республика Бурятия']

#reg_list = [f'{i:02d}' for i in range(1, 85)]

period_list = []
date = datetime.date(year=2018, month=1, day=1)
while str(datetime.date(year=END_YEAR, month=END_MONTH, day=1).strftime('%d%m%Y')) not in period_list:
    period_list.append(str(date.strftime('%d%m%Y')))
    date += relativedelta(years=1)

kd_code_list = ["00000000000000000", "10000000000000000", "20000000000000000"]

query_params = {"filterperiod": None, "filterperiodicity": "M", "pageSize": "1000", "filteroktmo.oktmoname": reg_list, "filterblocks.info": "PERKB", "FORMCODEOKUD": "0503317", "filterkd.code": kd_code_list}

data = []
for date in period_list:
    print(date, "Start")
    query_params["filterperiod"] = date
    resp = requests.get(endpoint, params=query_params)
    if resp.status_code == 200:
        data.append(resp.json())
    else:
        print(resp.status_code)
    print(date, "Done")


with open('output_yearly.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)