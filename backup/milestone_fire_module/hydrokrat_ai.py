import re
import streamlit as st
from app.pump_selector_engine import (
    build_response,
    get_fire_package
)
from app.rag_search import ask_hydrokrat_rag
import pandas as pd
from app.pdf_report import generate_report

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

    fire_type = None

    if application == "Fire Fighting":

        fire_type = st.selectbox(
            "Fire Type",
            [
                "Hydrant",
                "Sprinkler",
                "Hydrant + Sprinkler",
                "Jockey Pump"
            ]
        )

        project_name = st.text_input(
            "Project Name"
        )

        customer_name = st.text_input(
            "Customer Name"
        )

        consultant_name = st.text_input(
            "Consultant Name"
        )

        location = st.text_input(
            "Project Location"
        )
    fire_standard = None

    if fire_type == "Sprinkler":

        fire_standard = st.selectbox(
            "Fire Standard",
            [
                "Standard",
                "UL / NFPA 20",
                "FM",
                "VdS",
                "EN 12845"
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

    preferred_family = None

    if fire_type == "Sprinkler":

        if fire_standard in ["UL / NFPA 20", "FM"]:
            preferred_family = "Etanorm"

        elif fire_standard == "VdS":
            preferred_family = "MCPK"

        elif fire_standard == "EN 12845":
            preferred_family = "CPK"

    if application == "Fire Fighting":

        fire_package = get_fire_package(
            fire_type,
            flow_value,
            head_value,
            preferred_family
        )

    if fire_package:

        st.subheader("🔥 FIRE PUMP PACKAGE")
        if fire_type == "Sprinkler" and fire_standard:

            st.info(
                f"Selected Fire Standard: {fire_standard}"
            )
        family = "General Fire Pumps"

        if fire_standard in ["UL / NFPA 20", "FM"]:
            family = "Omega FXF / Etanorm FXM"

        elif fire_standard == "VdS":
            family = "Etanorm FXV / Multitec ASX / CPKN SX"

        elif fire_standard == "EN 12845":
            family = "Etanorm / Omega"

        st.success(
            f"Recommended KSB Family: {family}"
        )

        if preferred_family:

            st.warning(
                f"Preferred Family for {fire_standard}: {preferred_family}"
            )

        st.info(
            f"Requested Duty Point: {flow_value} m³/hr @ {head_value} m"
        )

        st.info(
            f"Selected KSB Package: {fire_package['flow']} m³/hr @ {fire_package['head']} m"
        )

        st.info(
            f"Pump Family: {fire_package['pump_family']}"
        )

        if fire_type == "Jockey Pump":

            st.success(
                f"🚒 Jockey Pump: {fire_package['jockey_pump']}"
            )

        pdf_file = generate_report(
            application=application,
            flow=flow_value,
            head=head_value,
            pumps=[],
            filename="fire_pump_report.pdf",
            fire_package=fire_package,
            fire_type=fire_type,
            fire_standard=fire_standard,
            project_name=project_name,
            customer_name=customer_name,
            consultant_name=consultant_name,
            location=location,
        )

        with open(pdf_file, "rb") as f:

            st.download_button(
                label="📄 Download Fire Pump Report",
                data=f,
                file_name="fire_pump_report.pdf",
                mime="application/pdf",
                key="fire_pdf"
            )    

            st.stop()

        st.subheader("🚒 MAIN ELECTRIC PUMP")

        st.write(
            f"**Model:** {fire_package['main_electric']}"
        )

        st.write(
            f"**Motor:** {fire_package['electric_motor']}"
        )

        st.subheader("🛢️ STANDBY DIESEL PUMP")

        st.write(
            f"**Model:** {fire_package['main_diesel']}"
        )

        st.write(
            f"**Engine:** {fire_package['diesel_engine']}"
        )

        st.subheader("🚒 JOCKEY PUMP")

        st.write(
            f"**Model:** {fire_package['jockey_pump']}"
        )
        result = build_response(
            application,
            flow_value,
            head_value
        )

        pumps = result.get("recommendations", [])

        if pumps:

            st.success("Recommended Pump Solutions")

            for idx, pump in enumerate(pumps):

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
                {"🏆 BEST MATCH" if idx == 0 else
                "🥈 SECOND CHOICE" if idx == 1 else
                "🥉 THIRD CHOICE" if idx == 2 else
                "⭐ ALTERNATIVE"}
                <br>
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
    # =========================
    # COMPARISON TABLE
    # =========================
#
#comparison_data = []
#
#for idx, pump in enumerate(pumps):
#
 #       rank = (
  #          "🏆" if idx == 0
  #          else "🥈" if idx == 1
  #          else "🥉" if idx == 2
  #          else "⭐"
 #       )
#
  #      comparison_data.append({
 #           "Rank": rank,
 #           "Pump": pump["pump_model"],
 #           "Confidence": pump["confidence"],
 #           "Motor": pump["motor_kw"],
  #          "Efficiency": pump["efficiency"]
 #       })

#st.subheader("📊 Pump Comparison")

#df = pd.DataFrame(comparison_data)

    #st.dataframe(
   #     df,
  #      use_container_width=True
  #  )
#
   # csv = df.to_csv(index=False)

  #  st.download_button(
  #      "📥 Download Comparison CSV",
   #     csv,
  #      "pump_comparison.csv",
   #     "text/csv",
   #     key="comparison_csv"
   # )
    # =========================
    # PDF REPORT
    # =========================

   # pdf_file = generate_report(
   #     application=application,
   #     flow=flow_value,
   #     head=head_value,
   #     pumps=pumps,
   #     filename="pump_report.pdf"
   # )
#
   # with open(pdf_file, "rb") as f:
#
   #     st.download_button(
  #           label="📄 Download Pump Selection Report",
   #          data=f,
   #          file_name="pump_report.pdf",
   #          mime="application/pdf",
   #          key="pump_pdf"
   # )

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