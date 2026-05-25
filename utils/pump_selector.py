import json


with open("data/pumps.json", "r") as file:

    pumps = json.load(file)


def calculate_score(pump, flow, head):

    flow_utilization = flow / pump["flow_max"]

    head_utilization = head / pump["head_max"]

    score = (
        abs(0.8 - flow_utilization) +
        abs(0.8 - head_utilization)
    )

    return score


def recommend_pumps(application, flow, head):

    matching_pumps = []

    for pump in pumps:

        # =========================
        # APPLICATION MATCH
        # =========================

        app_match = False

        for app in pump["application"]:

            if (
                application.lower() in app.lower()
                or
                app.lower() in application.lower()
            ):

                app_match = True

        if not app_match:

            continue

        # =========================
        # DUTY POINT CHECK
        # =========================

        if flow > pump["flow_max"]:

            continue

        if head > pump["head_max"]:

            continue

        # =========================
        # SCORE
        # =========================

        score = calculate_score(
            pump,
            flow,
            head
        )

        result = pump.copy()

        result["score"] = round(score, 2)

        matching_pumps.append(result)

    # =========================
    # SORT BEST MATCH
    # =========================

    matching_pumps.sort(
        key=lambda x: x["score"]
    )

    return matching_pumps[:5]