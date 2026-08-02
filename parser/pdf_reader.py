import os
import pdfplumber
import re

PDF_PATH = os.path.join("data", "Facultywise TT 20 sep.pdf")

if not os.path.exists(PDF_PATH):
    print("PDF not found!")
    exit()

teacher_list = []

with pdfplumber.open(PDF_PATH) as pdf:

    print(f"\nTotal Pages : {len(pdf.pages)}\n")

    for i, page in enumerate(pdf.pages):

        text = page.extract_text()

        if text is None:
            continue

        match = re.search(r"Teacher\s+(.+)", text)

        if match:
            teacher = match.group(1).strip()

            teacher_list.append(teacher)

            print(f"{i+1}. {teacher}")

print("\n----------------------------------")
print(f"Total Teachers Found : {len(teacher_list)}")