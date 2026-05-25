import re
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from utils.pump_selector import recommend_pumps

# =========================
# PUMP CURVE FUNCTION
# =========================


def generate_pump_curve(pump_name, max_flow, max_head, duty_flow, duty_head):
    flow = np.linspace(0, max_flow, 100)
    head = max_head * (1 - (flow / max_flow) ** 2)

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(flow, head, linewidth=3, label=pump_name)
    ax.scatter(
        duty_flow, duty_head, s=120, marker="o", color="red", label="Duty Point"
    )

    ax.set_xlabel("Flow (m³/hr)")
    ax.set_ylabel("Head (m)")
    ax.set_title(f"{pump_name} Performance Curve")
    ax.grid(True)
    ax.legend()
    return fig


# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Hydrokrat AI", page_icon="⚙️", layout="wide")

# =========================
# SESSION STATE
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================
# CLEAN UI CSS
# =========================
st.markdown(
    """
<style>
/* Hide Sidebar */
section[data-testid="stSidebar"] { display: none; }

/* Hide Streamlit Branding */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }

/* Main Background */
.main {
    background: linear-gradient(135deg, #f1f5f9, #dbeafe);
}

/* Main Container */
.block-container {
    max-width: 1000px;
    padding-top: 1rem;
}

/* Chat */
.stChatMessage {
    background: white;
    border-radius: 18px;
    padding: 14px;
    margin-bottom: 10px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.06);
}

/* Buttons */
.stButton > button {
    border-radius: 12px;
    background: #2563eb;
    color: white;
    border: none;
}

/* Inputs */
.stTextInput input {
    border-radius: 12px;
}
</style>
""",
    unsafe_allow_html=True,
)
# =========================
# HEADER
# =========================
header_html = """
<style>
/* Smooth pulsing glow for the blue outer border */
@keyframes pulseGlow {
    0% { box-shadow: 0 0 5px rgba(37,99,235,0.4); }
    50% { box-shadow: 0 0 25px rgba(37,99,235,0.9), 0 0 55px rgba(6,182,212,0.8); }
    100% { box-shadow: 0 0 5px rgba(37,99,235,0.4); }
}

/* This handles the smooth blinking fade effect for the pump image */
@keyframes pumpBlink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.15; } /* Drops opacity down to 15% at the lowest point */
}

.bot-wrapper {
    display: flex;
    align-items: center;
    gap: 25px;
    background: linear-gradient(135deg, #0f172a, #1e3a8a);
    padding: 30px;
    border-radius: 25px;
    margin-bottom: 25px;
}

.bot-circle {
    width: 130px;
    height: 130px;
    border-radius: 50%;
    background: white;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 5px solid #38bdf8;
    animation: pulseGlow 2s infinite;
}

/* This line forces the new pump icon image to loop the blink animation infinitely */
.bot-circle img {
    animation: pumpBlink 1.2s infinite ease-in-out;
}

.bot-title {
    color: white;
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 5px;
}

.bot-subtitle {
    color: #cbd5e1;
    font-size: 18px;
}
</style>

<div class="bot-wrapper">
    <div class="bot-circle">
        <img src="https://cdn-icons-png.flaticon.com/512/4115/4115041.png" width="72">
    </div>
    <div>
        <div class="bot-title">Hydrokrat AI</div>
        <div class="bot-subtitle">Smart Pump Selection & Engineering Assistant</div>
    </div>
</div>
"""

st.markdown(header_html, unsafe_allow_html=True)

# =========================
# QUICK PUMP SELECTOR
# =========================
st.subheader("🔧 Quick Pump Selection")

with st.form("pump_selector"):
    col1, col2, col3 = st.columns(3)
    with col1:
        application = st.selectbox(
            "Application",
            [
                "Fire Fighting",
                "HVAC",
                "Pressure Boosting",
                "Borewell",
                "Domestic Water",
                "Agriculture",
                "Drainage",
                "Sewage",
            ],
        )
    with col2:
        flow = st.text_input("Flow Rate (m³/hr)", placeholder="Example: 171")
    with col3:
        head = st.text_input("Head (m)", placeholder="Example: 70")

    submitted = st.form_submit_button("🚀 Recommend Pump")

# =========================
# QUICK SELECTOR RESULTS
# =========================
if submitted:
    try:
        flow_value = float(flow)
        head_value = float(head)
    except ValueError:
        st.error("Please enter valid numeric values.")
        st.stop()

    pumps = recommend_pumps(application, flow_value, head_value)

    if pumps:
        st.success("Recommended Pump Solutions")
        for pump in pumps[:3]:
            st.markdown(
                f"""
            <div style="background:white; padding:20px; border-radius:16px; margin-bottom:15px; box-shadow:0 4px 12px rgba(0,0,0,0.06); border-left:5px solid #2563eb;">
                <h3 style="color:#2563eb; margin-top:0;">⚙️ {pump["model"]}</h3>
                <p><b>Type:</b> {pump["type"]}</p>
                <p><b>Max Flow:</b> {pump["flow_max"]} m³/hr</p>
                <p><b>Max Head:</b> {pump["head_max"]} m</p>
                <p><b>Applications:</b> {", ".join(pump["application"][:3])}</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

            st.markdown("### ✅ Features")
            for feature in pump["features"]:
                st.markdown(f"- {feature}")

            curve_fig = generate_pump_curve(
                pump["model"],
                pump["flow_max"],
                pump["head_max"],
                flow_value,
                head_value,
            )
            st.pyplot(curve_fig)
    else:
        st.warning("No suitable pump found for this duty point.")

# =========================
# CHATBOT
# =========================
st.markdown("---")
st.subheader("💬 Hydrokrat AI Chat")

# Render historical messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "curve_data" in msg:
            fig = generate_pump_curve(*msg["curve_data"])
            st.pyplot(fig)

prompt = st.chat_input("Ask about pumps, HVAC, fire fighting, drainage...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        prompt_lower = prompt.lower()
        application = None

        # Application Detection Matrix
        if any(x in prompt_lower for x in ["fire", "hydrant", "sprinkler"]):
            application = "Fire Fighting"
        elif any(x in prompt_lower for x in ["hvac", "cooling", "chilled"]):
            application = "HVAC"
        elif any(
            x in prompt_lower
            for x in ["boost", "pressure", "hydropneumatic", "apartment"]
        ):
            application = "Pressure Boosting"
        elif any(
            x in prompt_lower
            for x in ["borewell", "submersible", "groundwater", "openwell"]
        ):
            application = "Borewell"
        elif any(x in prompt_lower for x in ["irrigation", "agriculture", "farm"]):
            application = "Agriculture"
        elif any(x in prompt_lower for x in ["sewage", "waste water"]):
            application = "Sewage"
        elif any(x in prompt_lower for x in ["drainage", "flood", "dewatering"]):
            application = "Drainage"
        elif any(x in prompt_lower for x in ["domestic", "home", "residential"]):
            application = "Domestic Water"

        # Parsing workflow values safely
        numbers = re.findall(r"\d+\.?\d*", prompt)
        flow_val = float(numbers[0]) if len(numbers) >= 2 else None
        head_val = float(numbers[1]) if len(numbers) >= 2 else None

        # Process matching
        if application and flow_val and head_val:
            pumps = recommend_pumps(application, flow_val, head_val)

            if pumps:
                response = "## ⚙️ Recommended Pump Solutions\n"
                pump = pumps[0]  # Show the best matched curve inside the chat

                response += f"### {pump['model']}\n"
                response += f"**Type:** {pump['type']}\n"
                response += f"**Max Flow:** {pump['flow_max']} m³/hr\n"
                response += f"**Max Head:** {pump['head_max']} m\n\n"
                response += "**Features:**\n- " + "\n- ".join(pump["features"])

                st.markdown(response)

                curve_params = (
                    pump["model"],
                    pump["flow_max"],
                    pump["head_max"],
                    flow_val,
                    head_val,
                )
                curve_fig = generate_pump_curve(*curve_params)
                st.pyplot(curve_fig)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": response,
                        "curve_data": curve_params,
                    }
                )
            else:
                response = "No suitable pump found for this duty point."
                st.markdown(response)
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )

        else:
            # Fallback static context matching
            engineering_answers = {
                "cavitation": """### Cavitation in Pumps\nCavitation occurs when pressure inside the pump falls below vapor pressure creating vapor bubbles.\n\nThese bubbles collapse violently causing:\n- Noise and vibration\n- Impeller damage\n- Seal damage\n- Reduced efficiency\n\n### Prevention\n- Proper NPSH\n- Correct suction piping\n- Proper pump selection""",
                "npsh": """### NPSH (Net Positive Suction Head)\nNPSH is the minimum suction pressure required to avoid cavitation.\n\nTwo types:\n- **NPSHa** → Available\n- **NPSHr** → Required\n\nFor safe operation:\n`NPSHa > NPSHr`""",
                "fire pump": """### Fire Fighting Pumps\nUsed for:\n- Hydrant systems\n- Sprinkler systems\n- Fire protection\n\nCommon KSB pumps:\n- Etanorm G\n- Etaline\n- Gamma/Omega\n- WK-WKS""",
            }

            response = None
            for key, value in engineering_answers.items():
                if key in prompt_lower:
                    response = value
                    break

            if response is None:
                response = """I can help with:
- Pump selection
- Fire fighting systems
- HVAC pumps
- Pressure boosting systems
- Borewell pumps
- Sewage pumps
- Drainage pumps
- Cavitation
- NPSH

Please provide structural metrics like: **Application**, **Flow**, and **Head**."""

            st.markdown(response)
            st.session_state.messages.append(
                {"role": "assistant", "content": response}
            )

# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown(
    '<div style="text-align:center; padding:20px; color:gray;">Powered by Hydrokrat AI Engineering Platform</div>',
    unsafe_allow_html=True,
)