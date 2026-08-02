import re


class IntentDetector:

    INTENTS = {

        "teacher_of_subject": [

            r"who teaches",
            r"faculty for",
            r"teacher of",
            r"who is teaching"
        ],

        "teacher_timetable": [

            r"timetable",
            r"schedule",
            r"classes of",
            r"lectures of"
        ],

        "faculty_free": [

            r"who is free",
            r"available faculty",
            r"free faculty"
        ],

        "room_free": [

            r"free room",
            r"free classroom",
            r"classroom available"
        ],

        "room_of_subject": [

            r"where is",
            r"which room",
            r"conducted"
        ]

    }

    @staticmethod
    def detect(question):

        question = question.lower()

        # Priority intents first
        priority = [
            "faculty_free",
            "room_free",
            "teacher_timetable",
            "teacher_of_subject",
            "room_of_subject"
        ]

        for intent in priority:

            for pattern in IntentDetector.INTENTS[intent]:

                if re.search(pattern, question):
                    return intent

        return "unknown"

        