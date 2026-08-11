import pdfplumber

FILE = r"data\Facultywise TT 20 sep.pdf"

print("=" * 80)
print("FIRST PAGE TEXT")
print("=" * 80)

with pdfplumber.open(FILE) as pdf:

    page = pdf.pages[0]

    text = page.extract_text()

    print(text)

print("=" * 80)