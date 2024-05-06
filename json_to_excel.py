import json
import pandas as pd

def json_to_excel(json_file, excel_file):
    """Read data from json file and save it to excel spreadsheet"""

    with open(json_file, 'r',  encoding='utf-8') as f:
        data = json.load(f)

    data_normalized = [pd.json_normalize(i) for i in data]
    df = pd.DataFrame(data_normalized)
    df.to_excel(excel_file, index=False)

json_to_excel('data1.json', 'output.xlsx')
