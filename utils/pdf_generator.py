from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf(
    filename,
    pump,
    application,
    flow,
    head,
    recommendation
):

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    story = []

    title = Paragraph(
        "Hydrokrat Pump Recommendation Report",
        styles['Title']
    )

    story.append(title)

    story.append(Spacer(1, 20))

    details = f"""
    <b>Pump Model:</b> {pump['model']}<br/>
    <b>Application:</b> {application}<br/>
    <b>Required Flow:</b> {flow} m3/hr<br/>
    <b>Required Head:</b> {head} m<br/>
    <b>Pump Type:</b> {pump['type']}<br/>
    """

    story.append(
        Paragraph(details, styles['BodyText'])
    )

    story.append(Spacer(1, 20))

    features = "<b>Features:</b><br/>"

    for feature in pump["features"]:

        features += f"• {feature}<br/>"

    story.append(
        Paragraph(features, styles['BodyText'])
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            recommendation,
            styles['BodyText']
        )
    )

    doc.build(story)