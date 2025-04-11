from pdf2image import convert_from_path
from google import genai
import easyocr
import numpy as np
import pdfplumber
import os

def extract_text(pdf_path, start=1, end=None):
    all_text = []
    non_text_count = 0
    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        end = min(end or total_pages, total_pages)
        
        for i in range(start - 1, end):
            page = pdf.pages[i]
            extracted_text = page.extract_text() or ""
            if not extracted_text.strip():
                non_text_count += 1
            else:
                non_text_count = 0
            
            # # If 3 consecutive pages have no text, raise an error
            # if non_text_count >= 3:
            #     raise ValueError(f"No text extracted from 3 consecutive pages starting from page {i - 1}")
            
            all_text.append(extracted_text)

    return "\n".join(all_text)

def extract_ocr(pdf_path, start=1, end=None):
    images = convert_from_path(pdf_path, dpi=300, first_page=start, last_page=end)
    reader = easyocr.Reader(['en'], gpu=True)

    all_text = []
    for img in images:
        img_np = np.array(img)
        result = reader.readtext(img_np)
        page_text = "\n".join([item[1] for item in result])
        all_text.append(page_text)

    return "\n".join(all_text)

def try_extract(pdf_path, start=1, end=None):
    try:
        return extract_text(pdf_path, start, end)
    except ValueError as e:
        print(f"{e}. Falling back to OCR.")
        return extract_ocr(pdf_path, start, end)

def extract_parse(pdf_path, start=1, end=None):
    extracted_text = extract_text(pdf_path, start, end) # no ocr for now, no ValueError
    filebasename = os.path.splitext(os.path.basename(pdf_path))[0]
    file_path = os.path.join(os.path.dirname(pdf_path), f"{filebasename}.txt")
    if os.path.exists(file_path):
        print(f"File {file_path} already exists. Skipping text extraction and data parsing.")
    else:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(extracted_text)
        print(f"Text extracted successfully and saved to {file_path}")

def parse(txt_path=''):
    file_path = os.path.join(txt_path, f"{year}.pdf")
    with open("output.txt", "w") as file:
        file.write(response)

if __name__ == "__main__":
    pdf_path = "examples/cvt24.pdf"
    start = 4
    end = 4

    extract_parse(pdf_path, start, end)
