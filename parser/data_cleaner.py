import re
from config.locations import KNOWN_LOCATIONS
from parser.components.cell_parser import CellParser

CLASS_PATTERN = r"^[1-9][A-Z0-9\- ]+$"


def parse_cell_old(cell):

    if not cell:
        return None

    cell = cell.strip()

    if cell == "":
        return None

    lines = [x.strip() for x in cell.split("\n") if x.strip()]

    result = {
        "subject": "",
        "room": "",
        "class": "",
        "group": "",
        "type": ""
    }

    subject_parts = []

    # longest locations first
    locations = sorted(KNOWN_LOCATIONS, key=len, reverse=True)

    for line in lines:

        # ---------------- GROUP ----------------
        if line.lower().startswith("group"):
            result["group"] = line
            continue

        # ---------------- CLASS ----------------
        if re.fullmatch(CLASS_PATTERN, line):
            class_name = line.strip()
            match = re.fullmatch(r"(\d+CS(?:AI|DS|IOT|E)?)([A-Z])", class_name)

            if match:
                class_name = f"{match.group(1)}-{match.group(2)}"

            result["class"] = class_name
            continue

        # ---------------- ROOM ----------------
        room_found = False

        # known locations
        for location in locations:
            if location.lower() == line.lower():
                result["room"] = location
                room_found = True
                break

        if room_found:
            continue

        # ---------------- Room inside subject ----------------
        for location in locations:

            if location.lower() in line.lower():

                result["room"] = location

                # Remove location from subject
                line = re.sub(
                    re.escape(location),
                    "",
                    line,
                    flags=re.IGNORECASE
                ).strip()
                # Remove extra spaces left after removing location
                line = re.sub(r"\s+", " ", line).strip()

                # Remove "(Group X)" if present
                group_match = re.search(
                    r"\s*\(Group\s+\d+\)",
                    line,
                    re.IGNORECASE
                )

                if group_match:
                    result["group"] = group_match.group().strip("() ").strip()

                line = re.sub(
                    r"\s*\(Group\s+\d+\)",
                    "",
                    line,
                    flags=re.IGNORECASE
                ).strip()

                room_found = True
                break

        
        # Remove any remaining CL-xx from subject
        line = re.sub(r"\bCL-\d+\b", "", line, flags=re.IGNORECASE)
        line = line.strip()


          # numeric room
        if not room_found:

            m = re.search(r"\b\d{3}\b", line)

            if m:
                result["room"] = m.group()

                line = line.replace(m.group(), "").strip()

        if line:
            subject_parts.append(line)

    result["subject"] = " ".join(subject_parts).strip()

    # ---------------- TYPE ----------------

    if "Lab" in result["subject"]:
        result["type"] = "Lab"

    elif "Seminar" in result["subject"]:
        result["type"] = "Seminar"

    elif "Project" in result["subject"]:
        result["type"] = "Project"

    else:
        result["type"] = "Theory"

    return result


def parse_cell(cell):

    result = CellParser.parse(cell)

    if result is None:
        return None

    subject = result["subject"].lower()

    if "lab" in subject:
        result["type"] = "Lab"

    elif "seminar" in subject:
        result["type"] = "Seminar"

    elif "project" in subject:
        result["type"] = "Project"

    else:
        result["type"] = "Theory"

    return result