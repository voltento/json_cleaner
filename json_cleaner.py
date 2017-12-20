#!/usr/bin/python3

import json
import sys

SPLITER = ":"


def inser_to_dictionary(dictionary, keys):
    if len(keys) == 0:
        return
    if keys[0] not in dictionary.keys():
        dictionary[keys[0]] = {}
    inser_to_dictionary(dictionary[keys[0]], keys[1:])


def filter_splice(splice: dict, filters: dict) -> dict:
    new_data = {}
    for k in filters.keys():
        if k in splice.keys():
            if len(filters[k]) == 0:
                new_data[k] = splice[k]
            else:
                new_data[k] = filter_splice(splice[k], filters[k])
    return new_data



if len(sys.argv) < 4:
    print("Expected params: [dictionary_file_path filter_file out_file]")
    exit(1)

# Parse filters
filters = {}
with open(sys.argv[2], "r") as f:
    print("Parsing filter file: '" + sys.argv[2] + "'...")
    for l in f:
        if len(l.rstrip()) > 0:
            keys = [v.rstrip() for v in l.split(SPLITER)]
            inser_to_dictionary(filters, keys)

# Load classificator
data = None
with open(sys.argv[1], "r") as f:
    print("Parsing json '" + sys.argv[1] + "'...")
    data = json.load(f)

# Clean classificator

filtred_data = filter_splice(data, filters)

with open(sys.argv[3], "w") as out:
    json.dump(filtred_data, out, indent=4, separators=(',', ': '), sort_keys=True)

print("Data saved to '" + sys.argv[3] + "'")
print("Completed")
