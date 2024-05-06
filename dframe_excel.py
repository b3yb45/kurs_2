import pandas as pd
import json
import time

start_time = time.time()

with open('output_monthly1.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    df = pd.json_normalize(data, record_path=['data'])
    df = df[['period','blockOktmo.oktmoname', 'blockOktmo.regioncode', 'blockKd.code', 'blockKd.name', 'blockStrcode.code', 'blockStrcode.name', 'perkb']]
    df.to_excel('output_monthly1.xlsx', index=False)

end_time = time.time()
print('Elapsed time:', end_time - start_time)
