import json

with open(
    "data/fire_pump_database.json",
    "r",
    encoding="utf-8"
) as f:

    pumps = json.load(f)

curve_map = {}

for pump in pumps:

    model = pump.get("main_electric")

    if model and model not in curve_map:

        curve_map[model] = ""

with open(
    "data/curve_mapping_template.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        curve_map,
        f,
        indent=4
    )

print(
    f"Created template for {len(curve_map)} pumps"
)