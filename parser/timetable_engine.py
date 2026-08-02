import os
import re
import json
import pdfplumber
from utils.validator import is_valid_teacher

PDF_PATH = os.path.join("data", "Facultywise TT 20 sep.pdf")
OUTPUT_FILE = os.path.join("database", "timetable.json")


DAY_MAP = {
    "Mo": "Monday",
    "Tu": "Tuesday",
    "We": "Wednesday",
    "Th": "Thursday",
    "Fr": "Friday",
    "Sa": "Saturday"
}


def parse_subject(cell):

    if cell is None:
        return None

    cell = cell.strip()

    if cell == "":
        return None

    lines = [x.strip() for x in cell.split("\n") if x.strip()]

    return lines


database = {}

with pdfplumber.open(PDF_PATH) as pdf:

    print("\nReading Faculty Timetable...\n")

    for page in pdf.pages:

        text = page.extract_text()

        if not text:
            continue

        teacher = re.search(r"Teacher\s+(.+)", text)

        if not teacher:
            continue

        teacher = teacher.group(1).strip()

        if not is_valid_teacher(teacher):
            print(f"Skipping invalid teacher on page: {teacher}")
            continue

        database[teacher] = {
            "Monday": [],
            "Tuesday": [],
            "Wednesday": [],
            "Thursday": [],
            "Friday": [],
            "Saturday": []
        }

        tables = page.extract_tables()

        if not tables:
            continue

        table = tables[0]

        for row in table[1:]:

            day = row[0]

            if day is None:
                continue

            day = day.strip()

            if day not in DAY_MAP:
                continue

            full_day = DAY_MAP[day]

            for slot in range(1,9):

                if slot >= len(row):
                    continue

                parsed = parse_subject(row[slot])

                if parsed:

                    database[teacher][full_day].append({

                        "slot": slot,

                        "raw": parsed

                    })


with open(OUTPUT_FILE,"w",encoding="utf-8") as f:

    json.dump(database,f,indent=4)

print("\nDatabase Saved Successfully")
print("Teachers :",len(database))