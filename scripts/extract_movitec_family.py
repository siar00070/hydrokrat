import re
import json
import pdfplumber

PDF_FILE = r"data/raw_pdf/KSB-Movitec; 50 Hz.PDF"

page_number = int(input("Enter page number: "))

with pdfplumber.open(PDF_FILE) as pdf:
    text = pdf.pages[page_number - 1].extract_text()

pattern = r"(\d+/\d+(?:-\d+)?)\s+(\d+,\d+)kW"

matches = re.findall(pattern, text)

pumps = []

for model, motor in matches:

    motor = float(motor.replace(",", "."))

    base_series = int(model.split("/")[0])

    pumps.append({
        "pump_model": model,
        "series": "Movitec",

        "flow_min": base_series - 10,
        "flow_max": base_series + 10,

        "head_min": 50,
        "head_max": 150,

        "bep_flow": base_series,
        "bep_head": 100,

        "motor_kw": motor,
        "efficiency": 80
    })

output_file = "data/generated/movitec_auto.json"

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(pumps, f, indent=4)

print(f"Found {len(pumps)} pumps")
print(f"Saved to {output_file}")

MASTER_DB = "data/generated/pump_master_database.json"

with open(MASTER_DB, "r", encoding="utf-8") as f:
    master = json.load(f)

existing = {pump.get("pump_model") for pump in master}

added = 0

for pump in pumps:
    if pump["pump_model"] not in existing:
        master.append(pump)
        added += 1

with open(MASTER_DB, "w", encoding="utf-8") as f:
    json.dump(master, f, indent=4)

print(f"Added {added} new pumps")
print(f"Database now contains {len(master)} pumps")