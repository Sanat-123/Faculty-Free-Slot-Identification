from parser.components.room_parser import RoomParser
from parser.components.class_parser import ClassParser
from parser.components.group_parser import GroupParser
from parser.components.subject_parser import SubjectParser


class LineParser:

    @staticmethod
    def parse(line):

        result = {
            "room": "",
            "class": "",
            "group": "",
            "subject": ""
        }

        line = line.strip()

        # Group
        group, line = GroupParser.extract(line)

        if group:
            result["group"] = group

        # Class
        class_name, line = ClassParser.extract(line)

        if class_name:
            result["class"] = class_name

        # Room
        room, line = RoomParser.extract(line)

        if room:
            result["room"] = room

        # Subject
        result["subject"] = SubjectParser.extract(line)

        return result