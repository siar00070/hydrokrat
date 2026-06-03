import os
import pandas as pd

PDF_FOLDER = "data/raw_pdf"

catalogues = []

for file in os.listdir(PDF_FOLDER):

    if not file.lower().endswith(".pdf"):
        continue

    application = "General"

    name = file.lower()

    if any(x in name for x in ["movitec", "hyaduo", "hyasolo", "moviboost", "delta"]):
        application = "Pressure Boosting"

    elif any(x in name for x in ["fire", "etanorm g", "wk", "wks"]):
        application = "Fire Fighting"

    elif any(x in name for x in ["etaline", "iln", "ilnc", "megaline", "calio"]):
        application = "HVAC"

    elif any(x in name for x in ["omega", "rdlo", "municipal"]):
        application = "Municipal Water"

    elif any(x in name for x in ["amarex", "amadrainer", "amaporter", "sewatec", "krt", "kwp"]):
        application = "Wastewater"

    elif any(x in name for x in ["upa", "uma", "submersible", "agri"]):
        application = "Agriculture / Borewell"

    catalogues.append({
        "catalogue_name": file,
        "application": application
    })

df = pd.DataFrame(catalogues)

output_file = "data/generated/catalogue_classification.xlsx"

df.to_excel(output_file, index=False)

print(f"Classified {len(df)} catalogues")
print(f"Saved: {output_file}")