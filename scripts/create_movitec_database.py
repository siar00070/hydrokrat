import json

pumps = [

    {
        "series": "Movitec",
        "model": "15/1",
        "flow_m3hr": 15,
        "motor_kw": 1.1,
        "rpm": 2900
    },

    {
        "series": "Movitec",
        "model": "15/2",
        "flow_m3hr": 15,
        "motor_kw": 2.2,
        "rpm": 2900
    },

    {
        "series": "Movitec",
        "model": "15/3",
        "flow_m3hr": 15,
        "motor_kw": 3.0,
        "rpm": 2900
    }

]

with open(
    "data/generated/pump_master_database.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        pumps,
        f,
        indent=4
    )

print("Database Created")
print(f"Models: {len(pumps)}")