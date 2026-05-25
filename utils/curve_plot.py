import json
import matplotlib.pyplot as plt


with open("data/curves.json", "r") as file:

    curves = json.load(file)


def plot_curve(pump_name, duty_flow, duty_head):

    if pump_name not in curves:

        return None

    curve = curves[pump_name]

    fig, ax = plt.subplots()

    ax.plot(
        curve["flow"],
        curve["head"],
        marker="o"
    )

    ax.scatter(
        duty_flow,
        duty_head,
        s=150
    )

    ax.set_title(f"{pump_name} Pump Curve")

    ax.set_xlabel("Flow (m3/hr)")

    ax.set_ylabel("Head (m)")

    ax.grid(True)

    return fig