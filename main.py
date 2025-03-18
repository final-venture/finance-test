from extract import extract
from fetch import fetch

pdf_path = "examples/cvt24.pdf"
raw_text = extract(pdf_path, start=4, end=4)
# print(raw_text)

with open('output.txt', 'w') as file:
    file.write(raw_text)


