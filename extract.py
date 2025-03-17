from pdf2image import convert_from_path
import pytesseract
import pdfplumber
import pandas as pd

def parse_ocr(pdf_path, start=1, end=None):
    images = convert_from_path(pdf_path, dpi=400, first_page=start, last_page=end)
    all_text = []
    for img in images:
        text = pytesseract.image_to_string(img)
        all_text.append(text)
    return "\n".join(all_text)

def parse_text(pdf_path, start=1, end=None):
    all_text = []
    with pdfplumber.open(pdf_path) as pdf:
        for i in range(start-1, end if end else len(pdf.pages)):
            page = pdf.pages[i]
            extracted_text = page.extract_text()
            if not extracted_text:
                raise ValueError(f"No text extracted from page {i + 1}")
            all_text.append(extracted_text)
    return "\n".join(all_text)

def parse(pdf_path, start=1, end=None):
    try:
        return parse_text(pdf_path, start, end)
    except ValueError as e:
        print(f"Failed to extract text with pdfplumber: {e}. Falling back to OCR.")
        # If scanned PDF, parse_ocr instead
        return parse_ocr(pdf_path, start, end)

pdf_path = "examples/cvt07.pdf"
raw_text = parse(pdf_path, start=5, end=5)
print(raw_text)

with open('output.txt', 'w') as file:
    file.write(raw_text)
