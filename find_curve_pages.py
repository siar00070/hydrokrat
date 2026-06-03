import json
import os

curve_map_file = "data/curve_mapping_template.json"

with open(curve_map_file, "r", encoding="utf-8") as f:
    curve_map = json.load(f)

for pump in curve_map.keys():
    print(pump)