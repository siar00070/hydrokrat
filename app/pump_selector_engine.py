import json
import os
from difflib import get_close_matches

DATA_DIR = "data"


def load_json(filename):
    path = os.path.join(DATA_DIR, filename)

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


CONFIG = load_json("chatbot_master_config.json")
SELECTION_RULES = load_json("pump_selection_rules.json")
AI_RULES = load_json("ai_recommendation_rules.json")


def load_database_files():
    all_pumps = []

    for file in CONFIG["database_files"]:
        try:
            data = load_json(file)

            if isinstance(data, list):
                all_pumps.extend(data)

        except Exception as e:
            print(f"Error loading {file}: {e}")

    return all_pumps


ALL_PUMPS = load_database_files()


def normalize(text):
    return text.lower().strip()


def find_application_rule(application):
    application = normalize(application)

    for rule in SELECTION_RULES:
        if normalize(rule["application"]) == application:
            return rule

    return None


def filter_by_application(application):
    rule = find_application_rule(application)

    if not rule:
        return []

    preferred = rule["preferred_pumps"]

    results = []

    for pump in ALL_PUMPS:
        series = pump.get("series", "")

        if series in preferred:
            results.append(pump)

    return results


def hydraulic_match(flow, head, pumps):
    matched = []

    for pump in pumps:

        flow_min = pump.get("flow_min")
        flow_max = pump.get("flow_max")

        head_min = pump.get("head_min")
        head_max = pump.get("head_max")

        if (
            flow_min is not None and
            flow_max is not None and
            head_min is not None and
            head_max is not None
        ):

            if (
                flow_min <= flow <= flow_max and
                head_min <= head <= head_max
            ):
                matched.append(pump)

    return matched


def rank_pumps(flow, head, pumps):

    ranked = []

    for pump in pumps:

        bep_flow = pump.get("bep_flow")
        bep_head = pump.get("bep_head")

        if bep_flow and bep_head:

            score = abs(flow - bep_flow) + abs(head - bep_head)

            ranked.append((score, pump))

    ranked.sort(key=lambda x: x[0])

    return [p[1] for p in ranked]


def get_ai_strengths(series):

    for item in AI_RULES:

        if item["series"] == series:
            return item.get("strengths", [])

    return []


def recommend_pumps(application, flow, head):

    application_pumps = filter_by_application(application)

    hydraulic_pumps = hydraulic_match(
        flow,
        head,
        application_pumps
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
            "message": "No suitable pump found for given duty point."
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

            "strengths":
                get_ai_strengths(
                    pump.get("series")
                )
        })

    return {
        "application": application,
        "required_flow": flow,
        "required_head": head,
        "recommendations": output
    }


if __name__ == "__main__":

    result = build_response(
        application="Fire Fighting",
        flow=171,
        head=70
    )

    print(json.dumps(result, indent=4))