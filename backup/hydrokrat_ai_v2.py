import re
import streamlit as st
from app.pump_selector_engine import build_response
from app.rag_search import ask_hydrokrat_rag

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Hydrokrat AI",
    page_icon="⚙️",
    layout="wide"
)

# =========================
# SESSION STATE
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================
# CLEAN UI
# =========================
st.markdown(
    """
    <style>

    section[data-testid="stSidebar"] {
        display: none;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    .main {
        background: linear-gradient(135deg, #f1f5f9, #dbeafe);
    }

    .block-container {
        max-width: 1000px;
        padding-top: 1rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# HEADER
# =========================
st.markdown(
    """
    <div style="
        background: linear-gradient(135deg,#0f172a,#1e3a8a);
        padding:30px;
        border-radius:20px;
        margin-bottom:25px;
        color:white;
    ">
        <h1>⚙️ Hydrokrat AI</h1>
        <p>Smart Pump Selection & Engineering Assistant</p>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================
# QUICK SELECTOR
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
                "Domestic Water Supply",
                "Agriculture",
                "Drainage & Dewatering",
                "Wastewater",
                "Industrial Process",
                "RO & Desalination"
            ]
        )

    with col2:
        flow = st.text_input(
            "Flow Rate (m³/hr)",
            placeholder="Example: 171"
        )

    with col3:
        head = st.text_input(
            "Head (m)",
            placeholder="Example: 70"
        )

    submitted = st.form_submit_button("🚀 Recommend Pump")

# =========================
# QUICK RESULTS
# =========================
if submitted:

    try:
        flow_value = float(flow)
        head_value = float(head)

    except ValueError:

        st.error("Please enter valid numeric values.")
        st.stop()

    result = build_response(
        application,
        flow_value,
        head_value
    )

    pumps = result.get("recommendations", [])

    if pumps:

        st.success("Recommended Pump Solutions")

        for pump in pumps:

            st.markdown(
                f"""
                <div style="
                    background:white;
                    padding:20px;
                    border-radius:16px;
                    margin-bottom:15px;
                    box-shadow:0 4px 12px rgba(0,0,0,0.06);
                    border-left:5px solid #2563eb;
                ">

                <h3 style="color:#2563eb;">
                    ⚙️ {pump["pump_model"]}
                </h3>

                <p><b>Series:</b> {pump["series"]}</p>

                <p><b>Flow Range:</b> {pump["flow_range"]}</p>

                <p><b>Head Range:</b> {pump["head_range"]}</p>

                <p><b>Efficiency:</b> {pump["efficiency"]}</p>

                <p><b>Confidence:</b> 🏆 {pump["confidence"]}</p>

                <p><b>Motor:</b> {pump["motor_kw"]}</p>

                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown("### ✅ Strengths")

            for strength in pump["strengths"]:
                st.markdown(f"- {strength}")

    else:

        st.warning(
            "No suitable pump found for this duty point."
        )

# =========================
# CHATBOT
# =========================
st.markdown("---")
st.subheader("💬 Hydrokrat AI Chat")

# Render history
for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input(
    "Ask about pumps, HVAC, fire fighting, NPSH..."
)

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        prompt_lower = prompt.lower()

        application = None

        # Application Detection
        if any(
            x in prompt_lower
            for x in ["fire", "hydrant", "sprinkler"]
        ):
            application = "Fire Fighting"

        elif any(
            x in prompt_lower
            for x in ["hvac", "cooling", "chilled"]
        ):
            application = "HVAC"

        elif any(
            x in prompt_lower
            for x in ["boost", "pressure"]
        ):
            application = "Pressure Boosting"

        elif any(
            x in prompt_lower
            for x in ["borewell", "submersible"]
        ):
            application = "Borewell"

        elif any(
            x in prompt_lower
            for x in ["sewage", "wastewater"]
        ):
            application = "Wastewater"

        elif any(
            x in prompt_lower
            for x in ["drainage", "dewatering"]
        ):
            application = "Drainage & Dewatering"

        # Parse numbers
        numbers = re.findall(r"\d+\.?\d*", prompt)

        flow_val = None
        head_val = None

        if len(numbers) >= 2:
            flow_val = float(numbers[0])
            head_val = float(numbers[1])

        # Engineering Selection
        if application and flow_val and head_val:

            result = build_response(
                application,
                flow_val,
                head_val
            )

            pumps = result.get("recommendations", [])

            if pumps:

                response = "## ⚙️ Recommended Pumps\n\n"

                for i, pump in enumerate(pumps, start=1):

                    response += f"""
### #{i} - {pump["pump_model"]}

**Series:** {pump["series"]}

**Flow Range:** {pump["flow_range"]}

**Head Range:** {pump["head_range"]}

**Efficiency:** {pump["efficiency"]}

**Confidence:** 🏆 {pump["confidence"]}

**Motor:** {pump["motor_kw"]}

**Strengths:**
"""

                    for s in pump["strengths"]:
                        response += f"\n- {s}"

                    response += "\n\n---\n"

            else:

                response = (
                    "No suitable pump found "
                    "for this duty point."
                )

        else:

            response = ask_hydrokrat_rag(prompt)

        st.markdown(response)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response
            }
        )

# =========================
# FOOTER
# =========================
st.markdown("---")

st.markdown(
    """
    <div style="
        text-align:center;
        color:gray;
        padding:20px;
    ">
    Powered by Hydrokrat AI Engineering Platform
    </div>
    """,
    unsafe_allow_html=True
)