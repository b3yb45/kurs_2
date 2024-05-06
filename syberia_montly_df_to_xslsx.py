import pandas as pd
import json

with open('output_syberia_monthly.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    df = pd.json_normalize(data, record_path=['data'])
    df.to_excel('syberia_output_monthly.xlsx')
