import json

FLOW_REQUIRED = 15
HEAD_REQUIRED = 82

with open(
    "data/generated/pump_master_database.json",
    "r",
    encoding="utf-8"
) as f:
    pumps = json.load(f)

matches = []

for pump in pumps:

    if pump["flow_m3hr"] >= FLOW_REQUIRED:

        if pump["head_m"] >= HEAD_REQUIRED:

            matches.append(pump)

matches = sorted(matches, key=lambda x: x["motor_kw"])

if matches:

    best = matches[0]

    print("\nRECOMMENDED PUMP")
    print("----------------")
    print(f"Series : {best['series']}")
    print(f"Model  : {best['model']}")
    print(f"Flow   : {best['flow_m3hr']} m3/hr")
    print(f"Head   : {best['head_m']} m")
    print(f"Motor  : {best['motor_kw']} kW")

else:

    print("No suitable pump found")