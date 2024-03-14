"""
json file to csv file
"""

import json
import sys

def json2xlsx(json_file, xlsx_file):
    import pandas as pd
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if not data:
        return
    if isinstance(data, list):
        df = pd.DataFrame(data)
    else:
        df = pd.DataFrame([data])
    df.to_excel(xlsx_file, index=False)

if __name__ == '__main__':
    json2xlsx(sys.argv[1], sys.argv[2])