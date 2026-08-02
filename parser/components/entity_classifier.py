import re

from parser.components.room_parser import RoomParser
from parser.components.class_parser import ClassParser
from parser.components.conflict_resolver import ConflictResolver


class EntityClassifier:

    @staticmethod
    def classify(tokens):

        result = {
            "room": "",
            "class": "",
            "group": "",
            "subject": []
        }

        i = 0

        while i < len(tokens):

            token = tokens[i]

            # ---------------- GROUP ----------------

            if token.lower() == "group":

                if i + 1 < len(tokens):
                    result["group"] = "Group " + tokens[i + 1]
                    i += 2
                    continue

            # ---------------- ROOM ----------------

            room, remaining = RoomParser.extract(token)

            if room:

                result["room"] = room

                if remaining:
                    result["subject"].append(remaining)

                i += 1
                continue

            # ---------------- CLASS ----------------

            class_name, remaining = ClassParser.extract(token)

            if class_name:

                result["class"] = class_name

                if remaining:
                    result["subject"].append(remaining)

                i += 1
                continue

            # ---------------- SUBJECT ----------------

            result["subject"].append(token)

            i += 1

        result["subject"] = " ".join(result["subject"]).strip()

        return ConflictResolver.resolve(result)