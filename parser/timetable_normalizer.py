import json
import re
import os
from config.locations import KNOWN_LOCATIONS

INPUT_FILE = os.path.join("database", "timetable.json")
OUTPUT_FILE = os.path.join("database", "clean_timetable.json")


def detect_room_number(subject):

    room = re.findall(r"[A-Z]*-?\d+", subject)

    if room:

        location = room[-1]

        subject = re.sub(r"[A-Z]*-?\d+", "", subject).strip()

        return subject, location

    return subject, ""
def detect_named_location(subject):

    if "IAI" not in subject.upper():
        return subject, ""

    print("\n==============================")
    print("Checking Subject:", repr(subject))

    original_subject = subject

    for location in sorted(KNOWN_LOCATIONS, key=len, reverse=True):

        print("Trying:", repr(location))

        pattern = re.compile(re.escape(location), re.IGNORECASE)

        match = pattern.search(subject)

        if match:

            print("MATCH FOUND:", repr(location))

            subject = pattern.sub("", subject).strip()

            subject = re.sub(r"\s{2,}", " ", subject)

            print("Remaining Subject:", repr(subject))

            return subject, location

    print("NO LOCATION FOUND")

    return original_subject, ""

def extract_location(subject):

    # Only debug problematic records
    if "IAI" in subject.upper() or "SEMINAR" in subject.upper():
        print("\n==============================")
        print("BEFORE :", repr(subject))

    # Step 1: Room number detector
    subject, location = detect_room_number(subject)

    if location:
        if "IAI" in subject.upper():
            print("ROOM FOUND :", location)
        return subject, location

    # Step 2: Named location detector
    subject, location = detect_named_location(subject)

    if "IAI" in subject.upper() or location:
        print("AFTER :", repr(subject))
        print("LOCATION :", repr(location))

    if location:
        return subject, location

    return subject, ""


def normalize(raw):
    data = {
        "subject": "",
        "room": "",
        "class": "",
        "group": "",
        "type": ""
    }

    # -------- THEORY --------
    if len(raw) == 2:
        class_name = raw[1].strip()

        # Remove spaces first
        class_name = class_name.replace(" ", "-")

        # Handle classes like 3CSAIA -> 3CS-AI-A
        match = re.fullmatch(r"(\d+)CS(AI|DS|IOT|E)?-?([A-Z])", class_name)

        if match:
            year = match.group(1)
            branch = match.group(2)
            section = match.group(3)

            if branch:
                class_name = f"{year}CS-{branch}-{section}"
            else:
                class_name = f"{year}CS-{section}"

        data["class"] = class_name

        subject = raw[0]

        # Extract location (room number, library, lab, hall, etc.)
        subject, location = extract_location(subject)

        if location:
            data["room"] = location

        subject = re.sub(r"\s*F:\s*$", "", subject).strip()

        data["subject"] = subject
        data["type"] = "Theory"
        return data

    # -------- LAB --------
    if len(raw) >= 3:
        room = re.findall(r"[A-Z]*-?\d+", raw[0])
        if room:
            data["room"] = room[-1]

        subject = re.sub(r"[A-Z]*-?\d+", "", raw[0]).strip()

        # Extract known locations from subject
        subject, location = detect_named_location(subject)

        if location:
            data["room"] = location

        subject = re.sub(r"\s*F:\s*$", "", subject).strip()
        data["subject"] = subject

        class_name = raw[1].strip()

        # Restore missing hyphen in simple class names like 3CSB -> 3CS-B
        match = re.fullmatch(r"(\d+CS(?:AI|DS|IOT|E)?)([A-Z])", class_name)
        if match:
            class_name = match.group(1) + "-" + match.group(2)

        if class_name.endswith("-"):
            data["class"] = class_name + raw[2].strip()
            data["group"] = ""
        else:
            data["class"] = class_name
            data["group"] = raw[2].strip()

        data["type"] = "Lab"
        if len(raw) >= 4 and raw[3]:
            data["room"] = raw[3]
        return data

    return data

with open(INPUT_FILE, encoding="utf-8") as file:
    database = json.load(file)

clean_database = {}

for teacher, days in database.items():
    clean_database[teacher] = {}
    for day, classes in days.items():
        clean_database[teacher][day] = []
        for lecture in classes:
            clean = normalize(lecture["raw"])
            clean["slot"] = lecture.get("slot")
            clean_database[teacher][day].append(clean)

with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    json.dump(clean_database, file, indent=4)

print("Clean Database Created Successfully")