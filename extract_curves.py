import fitz
import os

pdfs = {
    "etanorm": r"data\raw_pdf\KSB-50 Hz; Etanorm, Etanorm SYT, Etanorm V, (1).PDF",
    "mcpk": r"data\raw_pdf\KSB-50 Hz MegaCPK, HPK-L, Magnochem, Magnoch.PDF",
    "cpkn": r"data\raw_pdf\KSB-50HZ CPKN.PDF",
    "omega": r"data\raw_pdf\KSB-Omega _ Omega V.PDF"
}

for family, pdf_file in pdfs.items():

    print(f"\nProcessing {family}...")

    output_folder = f"assets/curves/{family}"
    os.makedirs(output_folder, exist_ok=True)

    pdf = fitz.open(pdf_file)

    for page_no in range(len(pdf)):

        page = pdf[page_no]

        pix = page.get_pixmap(
            matrix=fitz.Matrix(2, 2)
        )

        output_file = os.path.join(
            output_folder,
            f"page_{page_no + 1}.png"
        )

        pix.save(output_file)

    pdf.close()

    print(f"{family} exported")
    
print("\nDONE")