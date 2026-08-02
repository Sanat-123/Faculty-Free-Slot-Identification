from parser.components.line_parser import LineParser
from parser.components.type_parser import TypeParser


class CellParser:

    @staticmethod
    def parse(cell):

        if not cell:
            return None

        result = {
            "subject": "",
            "room": "",
            "class": "",
            "group": "",
            "type": ""
        }

        lines = [x.strip() for x in cell.split("\n") if x.strip()]

        for line in lines:

            parsed = LineParser.parse(line)

            if parsed["room"]:
                result["room"] = parsed["room"]

            if parsed["class"]:
                result["class"] = parsed["class"]

            if parsed["group"]:
                result["group"] = parsed["group"]

            if parsed["subject"]:

                if result["subject"]:
                    result["subject"] += " "

                result["subject"] += parsed["subject"]

        result["subject"] = " ".join(result["subject"].split())

        result["type"] = TypeParser.detect(result["subject"])

        return result