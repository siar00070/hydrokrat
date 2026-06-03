import pdfplumber

pdf_path = r"data/raw_pdf/KSB-Movitec; 50 Hz.PDF"

with pdfplumber.open(pdf_path) as pdf:

    for page_num in [42]:

        print("\n" + "=" * 80)
        print("PAGE:", page_num)

        text = pdf.pages[page_num - 1].extract_text()

        if text:
            print(text[:5000])
        else:
            print("NO TEXT FOUND")