import os
import json
import re
import pdfplumber
from parser.data_cleaner import parse_cell
from utils.validator import is_valid_teacher

PDF_PATH = os.path.join("data", "Facultywise TT 20 sep.pdf")
OUTPUT_FILE = os.path.join("database", "timetable.json")

timetable_database = {}

DAY_MAPPING = {
    "Mo": "Monday",
    "Tu": "Tuesday",
    "We": "Wednesday",
    "Th": "Thursday",
    "Fr": "Friday",
    "Sa": "Saturday"
}


with pdfplumber.open(PDF_PATH) as pdf:

    for page in pdf.pages:

        text = page.extract_text()

        if not text:
            continue

        teacher_match = re.search(r"Teacher\s+(.+)", text)

        if not teacher_match:
            continue

        teacher = teacher_match.group(1).strip()

        if "Mamta" in teacher:
            print("\n========== FOUND MAMTA ==========")
            print("Teacher:", repr(teacher))

        if not is_valid_teacher(teacher):
            print(f"Skipping invalid teacher: {teacher}")
            continue

        timetable_database[teacher] = {
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
        print("\n========== COMPLETE TABLE ==========")

        for row in table:
         print(row)

        print("====================================")
        if "Mamta" in teacher:
            print("Rows in table:", len(table))
            for row in table:
                print(row)

        print(f"\nTeacher : {teacher}")
        print(f"Rows : {len(table)}")

        for row in table[1:]:

            if not row:
                continue

            day = row[0]

            if day not in DAY_MAPPING:
                continue

            full_day = DAY_MAPPING[day]

            for slot in range(1, 9):

                if slot >= len(row):
                    continue

                cell = row[slot]

                if not cell:
                    continue

                print("\n---------------------------")
                print("Teacher :", teacher)
                print("Day     :", full_day)
                print("Slot    :", slot)
                print("CELL:")
                print(repr(cell))
                print("---------------------------")

                parsed_data = parse_cell(cell)

                if parsed_data:
                    timetable_database[teacher][full_day].append({
                        "slot": slot,
                        **parsed_data
                    })



with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    json.dump(timetable_database, file, indent=4)

print("\nTimetable Database Created Successfully!")
print("Teachers :", len(timetable_database))