from pdf2image import convert_from_path
import numpy as np
import easyocr
import pdfplumber

def parse_ocr(pdf_path, start=1, end=None):
    images = convert_from_path(pdf_path, dpi=300, first_page=start, last_page=end)
    reader = easyocr.Reader(['en'], gpu=True)
    
    all_text = []
    for img in images:
        img_np = np.array(img)
        
        result = reader.readtext(img_np)
        
        page_text = "\n".join([item[1] for item in result])
        all_text.append(page_text)
    
    return "\n".join(all_text)

def parse_text(pdf_path, start=1, end=None):
    all_text = []
    non_text_count = 0
    with pdfplumber.open(pdf_path) as pdf:
        for i in range(start-1, end if end else len(pdf.pages)):
            page = pdf.pages[i]
            extracted_text = page.extract_text()
            if not extracted_text:
                non_text_count += 1
            else:
                non_text_count = 0
            
            # If 5 consecutive pages have no text, raise an error
            if non_text_count >= 3:
                raise ValueError(f"No text extracted from 3 consecutive pages starting from page {i - 2}")
            all_text.append(extracted_text)
    return "\n".join(all_text)

def parse(pdf_path, start=1, end=None):
    try:
        return parse_text(pdf_path, start, end)
    except ValueError as e:
        print(f"{e}. Falling back to OCR.")
        # If scanned PDF, parse_ocr instead
        return parse_ocr(pdf_path, start, end)
