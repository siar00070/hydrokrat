from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_report(application, flow, head, pumps, filename="pump_report.pdf"):

    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "Hydrokrat AI Pump Selection Report",
            styles["Title"]
        )
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(f"Application: {application}", styles["Normal"])
    )

    content.append(
        Paragraph(f"Flow: {flow} m3/hr", styles["Normal"])
    )

    content.append(
        Paragraph(f"Head: {head} m", styles["Normal"])
    )

    content.append(Spacer(1, 12))

    if pumps:

        best = pumps[0]

        content.append(
            Paragraph("Best Match", styles["Heading2"])
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
                Paragraph("Alternative Pumps", styles["Heading2"])
            )

            for pump in pumps[1:]:

                content.append(
                    Paragraph(
                        f"{pump['pump_model']} | {pump['confidence']} | {pump['motor_kw']}",
                        styles["Normal"]
                    )
                )

    doc.build(content)

    return filename

