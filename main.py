import extract

pdf_path = "examples/cvt07.pdf"
raw_text = extract.parse(pdf_path, start=5, end=5)
print(raw_text)

with open('output.txt', 'w') as file:
    file.write(raw_text)
    