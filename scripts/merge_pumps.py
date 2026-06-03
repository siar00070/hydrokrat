import json

MASTER_DB = "data/generated/pump_master_database.json"
NEW_PUMPS = "data/generated/movitec_auto.json"

with open(MASTER_DB, "r", encoding="utf-8") as f:
    master = json.load(f)

with open(NEW_PUMPS, "r", encoding="utf-8") as f:
    new = json.load(f)

existing = {
    pump.get("pump_model")
    for pump in master
}

added = 0

for pump in new:

    if pump["pump_model"] not in existing:
        master.append(pump)
        added += 1

with open(MASTER_DB, "w", encoding="utf-8") as f:
    json.dump(master, f, indent=4)

print(f"Added {added} pumps")
print(f"Database now contains {len(master)} pumps")