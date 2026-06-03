import json
import os

APPLICATION_RULES = {

        "Pressure Boosting": ["Movitec"],

        "HVAC": ["Etaline"],

        "Fire Fighting": ["Etanorm", "Omega"],

        "Domestic Water Supply": ["Delta", "Movitec"],

        "Borewell": ["Submersible"],

        "Drainage & Dewatering": ["AmaDrainer"],

        "Wastewater": ["AmaDrainer"],

        "Agriculture": ["Submersible"],

        "Industrial Process": ["Movitec"],

        "RO & Desalination": ["Movitec"]
    }
DATA_DIR = "data"


def load_json(filename):
    path = os.path.join(DATA_DIR, filename)

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# Load pump database
ALL_PUMPS = load_json(
    "generated/pump_master_database.json"
)

FIRE_PUMPS = []

try:
    with open(
        "data/fire_pump_database.json",
        "r",
        encoding="utf-8"
    ) as f:

        FIRE_PUMPS = json.load(f)

except Exception:
    FIRE_PUMPS = []

for pump in FIRE_PUMPS:

    if "pump_family" not in pump:

        model = pump.get(
            "main_electric",
            ""
        )

        if model.startswith("ETN"):
            pump["pump_family"] = "Etanorm"

        elif model.startswith("MCPK"):
            pump["pump_family"] = "MCPK"

        elif model.startswith("CPK"):
            pump["pump_family"] = "CPK"

        else:
            pump["pump_family"] = "Unknown"

def hydraulic_match(flow, head, pumps):

    matched = []

    for pump in pumps:

        flow_min = pump.get("flow_min", 0)
        flow_max = pump.get("flow_max", 0)

        head_min = pump.get("head_min", 0)
        head_max = pump.get("head_max", 0)

        if (
            flow_min * 0.9 <= flow <= flow_max * 1.1
            and
            head_min * 0.9 <= head <= head_max * 1.1
        ):
            matched.append(pump)

    # Exact matches found
    if len(matched) >= 3:
        return matched

    # -------------------------
    # Find nearest alternatives
    # -------------------------
    alternatives = []

    for pump in pumps:

        bep_flow = pump.get("bep_flow", 0)
        bep_head = pump.get("bep_head", 0)

        distance = (
            abs(flow - bep_flow)
            +
            abs(head - bep_head)
        )

        alternatives.append(
            (distance, pump)
        )

    alternatives.sort(
        key=lambda x: x[0]
    )

    for _, pump in alternatives:

        if pump not in matched:
            matched.append(pump)

        if len(matched) >= 5:
            break

    return matched

def rank_pumps(flow, head, pumps, application=None):

    ranked = []

    preferred_series = APPLICATION_RULES.get(
        application,
        []
    )

    for pump in pumps:

        bep_flow = pump.get("bep_flow", 0)
        bep_head = pump.get("bep_head", 0)

        hydraulic_score = (
            abs(flow - bep_flow)
            + abs(head - bep_head)
        )

        bonus = 0

        if pump.get("series") in preferred_series:
            bonus = 20

        efficiency = pump.get(
            "efficiency",
            80
        )

        score = (
            hydraulic_score
            - bonus
            - (efficiency / 10)
        )

        confidence = max(
            50,
            min(
                100,
                100 - int(hydraulic_score / 2)
            )
        )

        pump["confidence"] = f"{confidence}%"

        ranked.append(
            (score, pump)
        )

    ranked.sort(
        key=lambda x: x[0]
    )

    return [item[1] for item in ranked]

def recommend_pumps(application, flow, head):

    hydraulic_pumps = hydraulic_match(
        flow,
        head,
        ALL_PUMPS
    )

    preferred_series = APPLICATION_RULES.get(
         application,
         []
    )

    if preferred_series:

         hydraulic_pumps = [
            p for p in hydraulic_pumps
            if p.get("series") in preferred_series
         ]

    ranked = rank_pumps(
        flow,
        head,
        hydraulic_pumps,
        application
    )

    unique = []
    seen = set()

    for pump in ranked:

        base_model = pump["pump_model"].split("-")[0]

        if base_model not in seen:
            unique.append(pump)
            seen.add(base_model)

    return unique[:5]


def build_response(application, flow, head):

    recommendations = recommend_pumps(
        application,
        flow,
        head
    )
    
    if not recommendations:

        return {
            "status": "No Match Found",
            "message": "No suitable pump found for given duty point.",
            "recommendations": []
        }

    output = []

    for pump in recommendations:

        output.append({

            "pump_model": pump.get("pump_model"),

            "series": pump.get("series"),

            "flow_range":
                f"{pump.get('flow_min')} - {pump.get('flow_max')} m3/hr",

            "head_range":
                f"{pump.get('head_min')} - {pump.get('head_max')} m",

            "efficiency":
                f"{pump.get('efficiency')} %",

            "motor_kw":
                f"{pump.get('motor_kw')} kW",

            "confidence": pump["confidence"],

            "strengths": [
                "High efficiency",
                "Reliable operation",
                "Suitable for pressure boosting"
            ]
        })

    return {
        "application": application,
        "required_flow": flow,
        "required_head": head,
        "recommendations": output
    }


if __name__ == "__main__":

    result = build_response(
        application="Pressure Boosting",
        flow=125,
        head=120
    )

    print(json.dumps(result, indent=4))

def get_fire_package(
    fire_type,
    flow,
    head,
    preferred_family=None
):

    if not FIRE_PUMPS:
        return None

    candidates = [
        item
        for item in FIRE_PUMPS
        if item.get("fire_type") == fire_type
    ]

    if preferred_family:

        family_matches = [
            item
            for item in candidates
            if item.get("pump_family") == preferred_family
        ]

        if family_matches:
            candidates = family_matches

    if not candidates:
        return None

    suitable = []

    for item in candidates:

        if (
            item["flow"] >= flow
            and item["head"] >= head
        ):
            suitable.append(item)

    if suitable:

        suitable.sort(
            key=lambda x: (
                x["flow"] - flow
                + x["head"] - head
            )
        )

        return suitable[0]

    best_match = None
    best_score = 999999

    for item in candidates:

        score = (
            abs(flow - item["flow"])
            + abs(head - item["head"])
        )

        if score < best_score:
            best_score = score
            best_match = item

    return best_match