

def csv2json(csv_file, json_file):
    import csv
    import json

    with open(csv_file) as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    with open(json_file, 'w') as f:
        json.dump(rows, f, indent=4)