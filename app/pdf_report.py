from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
import os
import json

def generate_report(
    application,
    flow,
    head,
    pumps,
    filename="pump_report.pdf",
    fire_package=None,
    fire_type=None,
    fire_standard=None,
    project_name="",
    customer_name="",
    consultant_name="",
    location=""
):

    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    content = []

    # =================================
    # REPORT HEADER
    # =================================

    logo_path = "assets/logo.png"

    if os.path.exists(logo_path):

        content.append(
            Image(
                logo_path,
                width=260,
                height=70
            )
        )

    content.append(Spacer(1, 20))
  
    content.append(
        Paragraph(
            "PUMP SELECTION REPORT",
            styles["Heading1"]
        )
    )

    content.append(Spacer(1, 30))

    content.append(
        Paragraph(
            f"<b>Project Name:</b> {project_name}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Customer Name:</b> {customer_name}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Consultant Name:</b> {consultant_name}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Project Location:</b> {location}",
            styles["Normal"]
        )
    )

    content.append(Spacer(1, 20))

    content.append(
        Paragraph(
            f"<b>Application:</b> {application}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Duty Point:</b> {flow} m³/hr @ {head} m",
            styles["Normal"]
        )
    )

    content.append(Spacer(1, 250))

    content.append(
        Paragraph(
            "Prepared by Hydrokrat AI",
            styles["Italic"]
        )
    )

    content.append(PageBreak())

    content.append(
        Paragraph(
            "Hydrokrat AI Pump Selection Report",
            styles["Title"]
        )
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            f"Application: {application}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Flow: {flow} m³/hr",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Head: {head} m",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Report Date: {datetime.now().strftime('%d-%m-%Y %H:%M')}",
            styles["Normal"]
        )
    )

    content.append(Spacer(1, 12))

    # =================================
    # FIRE FIGHTING REPORT
    # =================================

    if application == "Fire Fighting" and fire_package:

        content.append(
            Paragraph(
                "Fire Pump Selection",
                styles["Heading2"]
            )
        )

        content.append(
            Paragraph(
                f"Fire Type: {fire_type}",
                styles["Normal"]
            )
        )

        if fire_standard:

            content.append(
                Paragraph(
                    f"Fire Standard: {fire_standard}",
                    styles["Normal"]
                )
            )

        content.append(
            Paragraph(
                f"Requested Duty Point: {flow} m³/hr @ {head} m",
                styles["Normal"]
            )
        )

        content.append(
            Paragraph(
                f"Selected Package: {fire_package['flow']} m³/hr @ {fire_package['head']} m",
                styles["Normal"]
            )
        )

        content.append(
            Paragraph(
                f"Pump Family: {fire_package['pump_family']}",
                styles["Normal"]
            )
        )

        content.append(
            Paragraph(
                f"Main Electric Pump: {fire_package['main_electric']}",
                styles["Normal"]
            )
        )

        content.append(
            Paragraph(
                f"Motor: {fire_package['electric_motor']}",
                styles["Normal"]
            )
        )

        content.append(
            Paragraph(
                f"Standby Diesel Pump: {fire_package['main_diesel']}",
                styles["Normal"]
            )
        )

        content.append(
            Paragraph(
                f"Diesel Engine: {fire_package['diesel_engine']}",
                styles["Normal"]
            )
        )

        content.append(
            Paragraph(
                f"Jockey Pump: {fire_package['jockey_pump']}",
                styles["Normal"]
            )
        )

        curve_file = None

        try:

            with open(
                "data/curve_mapping.json",
                "r",
                encoding="utf-8"
            ) as f:

                curve_map = json.load(f)

            curve_file = curve_map.get(
                fire_package["main_electric"]
            )

        except Exception as e:

            print("Curve Mapping Error:", e)

            curve_file = None
        
        if curve_file and os.path.exists(curve_file):

            content.append(Spacer(1, 20))

            content.append(
                Paragraph(
                    "Pump Performance Curve",
                    styles["Heading2"]
                )
            )

            content.append(
                Image(
                    curve_file,
                    width=450,
                    height=320
                )
            )

    # =================================
    # NORMAL PUMP REPORT
    # =================================

    elif pumps:

        best = pumps[0]

        content.append(
            Paragraph(
                "Best Match",
                styles["Heading2"]
            )
        )

        content.append(
            Paragraph(
                f"{best['pump_model']} | {best['confidence']} | {best['motor_kw']}",
                styles["Normal"]
            )
        )

        content.append(Spacer(1, 12))

        if len(pumps) > 1:

            content.append(
                Paragraph(
                    "Alternative Pumps",
                    styles["Heading2"]
                )
            )

            for pump in pumps[1:]:

                content.append(
                    Paragraph(
                        f"{pump['pump_model']} | {pump['confidence']} | {pump['motor_kw']}",
                        styles["Normal"]
                    )
                )

    # =================================
    # FOOTER
    # =================================

    content.append(Spacer(1, 20))

    content.append(
        Paragraph(
            "Hydrokrat Pumps & Engineering Solutions",
            styles["Heading3"]
        )
    )

    content.append(
        Paragraph(
            "AI Powered KSB Pump Selection Platform",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            "www.hydrokratpumps.in",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            "Generated by Hydrokrat AI",
            styles["Italic"]
        )
    )

    # =================================
    # BUILD PDF
    # =================================

    doc.build(content)

    return filename