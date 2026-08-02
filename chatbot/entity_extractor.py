import re

from parser.components.class_parser import ClassParser
from parser.components.group_parser import GroupParser
from parser.components.room_parser import RoomParser


class EntityExtractor:

    DAYS = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday"
    ]

    @staticmethod
    def extract(question):

        result = {
            "teacher": "",
            "subject": "",
            "class": "",
            "group": "",
            "day": "",
            "slot": "",
            "room": ""
        }

        text = question

        # ---------- Class ----------
        class_name, text = ClassParser.extract(text)

        result["class"] = class_name

        # ---------- Group ----------
        group, text = GroupParser.extract(text)

        result["group"] = group

        # ---------- Room ----------
        room, text = RoomParser.extract(text)

        result["room"] = room

        # ---------- Day ----------
        for day in EntityExtractor.DAYS:

            if day.lower() in text.lower():

                result["day"] = day

                text = re.sub(
                    day,
                    "",
                    text,
                    flags=re.IGNORECASE
                )

                break

        # ---------- Slot ----------
        m = re.search(r"Slot\s+(\d+)", text, re.IGNORECASE)

        if m:

            result["slot"] = int(m.group(1))

            text = re.sub(
                r"Slot\s+\d+",
                "",
                text,
                flags=re.IGNORECASE
            )

        # ---------- Remove common question words ----------
        REMOVE_PATTERNS = [

            r"\bwho teaches\b",
            r"\bteacher of\b",
            r"\bfaculty for\b",
            r"\bwhere is\b",
            r"\bconducted\b",
            r"\bshow timetable of\b",
            r"\btimetable of\b",
            r"\bshow\b",
            r"\bin\b",
            r"\bof\b",
            r"\?\s*$"
        ]

        for pattern in REMOVE_PATTERNS:

            text = re.sub(
                pattern,
                "",
                text,
                flags=re.IGNORECASE
            )

        text = " ".join(text.split())

        result["subject"] = text

        return result