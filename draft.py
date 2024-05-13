import requests
import json
import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import time

END_YEAR = 2024
END_MONTH = 4

endpoint = 'http://budget.gov.ru/epbs/registry/7710568760-repexecutincome/data'

oktmoname_list = ['Республика Алтай', 'Республика Тыва', 'Республика Хакасия', 'Алтайский край', 'Красноярский край', 'Иркутская область', 'Кемеровская область - Кузбасс', 'Новосибирская область', 'Омская область', 'Томская область', 'Республика Бурятия']

reg_code_list = [f'{i:02d}' for i in range(1, 91)]

period_list = []
date = datetime.date(year=2018, month=1, day=1)
while str(datetime.date(year=END_YEAR, month=END_MONTH, day=1).strftime('%d%m%Y')) not in period_list:
    period_list.append(str(date.strftime('%d%m%Y')))
    date += relativedelta(months=1)

kd_code_list = ["00000000000000000",
                "10000000000000000",
                "10100000000000000",
                "10101000000000110",
                "10102000010000110",
                "10300000000000000",
                "10500000000000000",
                "10600000000000000",
                "10700000000000000",
                "10800000000000000",
                "10900000000000000",
                "11100000000000000",
                "11200000000000000",
                "11300000000000000",
                "11400000000000000",
                "11500000000000000",
                "11600000000000000",
                "11700000000000000",
                "20000000000000000",
                "20200000000000000",
                "20210000000000150",
                "20220000000000150",
                "20230000000000150",
                "20240000000000150",
                "20250000000000150",
                "20290000000000150",
                "20300000000000000",
                "20400000000000000",
                "20700000000000000",
                "21800000000000000"]

query_params = {"filterperiod": None, "filterperiodicity": "M", "pageSize": "1000", "filteroktmo.oktmoname": oktmoname_list, "filterblocks.info": "PERKB", "FORMCODEOKUD": "0503317", "filterkd.code": kd_code_list}


start_time = time.time()
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
end_time = time.time()
print("Elapsed time:", end_time - start_time)

with open('kbfo_mrs_draft.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

df = pd.json_normalize(data, record_path=['data'])
budget = df[['period','blockOktmo.oktmoname', 'blockOktmo.regioncode', 'blockKd.code', 'blockKd.name', 'blockStrcode.code', 'blockStrcode.name', 'perkb']]
filt = ((df['blockKd.name'] == 'Доходы бюджета - всего, в том числе:') | (df['blockStrcode.name'] == 'Доходы бюджета - всего, в том числе:'))
budget.drop(index=df[filt].index, inplace=True)
budget.to_excel('kbfo_mrs_draft.xlsx', index=False)
