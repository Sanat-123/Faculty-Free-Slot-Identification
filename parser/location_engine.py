import os
import pdfplumber

PDF_PATH = os.path.join(
    "data",
    "Location wise TT 27 sep 2025.pdf"
)

with pdfplumber.open(PDF_PATH) as pdf:

    print("=" * 60)
    print("LOCATION PDF READER")
    print("=" * 60)

    print("Pages :", len(pdf.pages))

    page = pdf.pages[0]
    print("=" * 60)
    print("FULL PAGE TEXT")
    print("=" * 60)

    text = page.extract_text()

print(text)

import re

room = re.search(r"\n(\d{3}|CP\d+|CL-\d+)\.?\n", text)

if room:
    print("\nROOM FOUND :", room.group(1))
else:
    print("\nROOM NOT FOUND")
    tables = page.extract_tables()

    print("Tables :", len(tables))

    for i, table in enumerate(tables):

        print("\nTABLE", i + 1)

        for row in table:
            print(row)