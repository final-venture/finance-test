from pdf2image import convert_from_path
import pytesseract
import pandas as pd

def ocr_pdf_to_text(pdf_path):
    images = convert_from_path(pdf_path, dpi=400)
    all_text = []
    for img in images:
        text = pytesseract.image_to_string(img)
        all_text.append(text)
    return "\n".join(all_text)

pdf_path = "examples/cvt24.pdf"
raw_text = ocr_pdf_to_text(pdf_path)
print(raw_text)

with open('output.txt', 'w') as file:
    file.write(raw_text)
