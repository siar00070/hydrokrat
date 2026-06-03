import json
import os

DATA_DIR = "data"


def load_json(filename):
    path = os.path.join(DATA_DIR, filename)

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# Load pump database
ALL_PUMPS = load_json(
    "generated/pump_master_database.json"
)


def hydraulic_match(flow, head, pumps):

    matched = []

    for pump in pumps:

        flow_min = pump.get("flow_min", 0)
        flow_max = pump.get("flow_max", 0)

        head_min = pump.get("head_min", 0)
        head_max = pump.get("head_max", 0)

        if (
            flow_min <= flow <= flow_max
            and
            head_min <= head <= head_max
        ):
            matched.append(pump)

    return matched


def rank_pumps(flow, head, pumps):

    ranked = []

    for pump in pumps:

        bep_flow = pump.get("bep_flow", 0)
        bep_head = pump.get("bep_head", 0)

        score = abs(flow - bep_flow) + abs(head - bep_head)

        ranked.append((score, pump))

    ranked.sort(key=lambda x: x[0])

    return [item[1] for item in ranked]


def recommend_pumps(application, flow, head):

    hydraulic_pumps = hydraulic_match(
        flow,
        head,
        ALL_PUMPS
    )

    ranked = rank_pumps(
        flow,
        head,
        hydraulic_pumps
    )

    return ranked[:5]


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