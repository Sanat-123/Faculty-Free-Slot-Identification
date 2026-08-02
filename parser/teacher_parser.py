import os
import re
import json
import pdfplumber
from utils.validator import is_valid_teacher

PDF_PATH = os.path.join("data", "Facultywise TT 20 sep.pdf")
OUTPUT_FILE = os.path.join("database", "faculty_database.json")

faculty_database = {}

with pdfplumber.open(PDF_PATH) as pdf:

    for page_number, page in enumerate(pdf.pages, start=1):

        text = page.extract_text()

        if not text:
            continue

        match = re.search(r"Teacher\s+(.+)", text)

        if match:

            teacher = match.group(1).strip()
            if not is_valid_teacher(teacher):
             print(f"Skipping invalid teacher on page {page_number}: {teacher}")
            continue
            
            print(f"Page {page_number}: {teacher}")

            faculty_database[teacher] = {
                "page": page_number
            }

with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    json.dump(faculty_database, file, indent=4)

print("Faculty Database Created Successfully")
print("Total Faculty :", len(faculty_database))