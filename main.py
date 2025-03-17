import pdfplumber

pdf_path = "examples/cvt24.pdf"
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            print(table)
