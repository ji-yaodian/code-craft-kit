"""
json file to csv file
"""

import json
import csv

import sys


def json2csv(json_file, csv_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if not data:
        return
    if isinstance(data, list):
        keys = data[0].keys()
    else:
        keys = data.keys()
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, keys)
        writer.writeheader()
        if isinstance(data, list):
            writer.writerows(data)
        else:
            writer.writerow(data)


if __name__ == '__main__':
    json2csv(sys.argv[1], sys.argv[2])
