class IntentDetector:
    """
    Rule-based Intent Detector.

    Uses:
    - keywords
    - extracted entities
    - extracted day/slot

    No fuzzy sentence matching.
    """

    INTENT_RULES = {

        "FIND_TEACHER": {
            "keywords": {
                "teach",
                "teaches",
                "teacher",
                "faculty"
            }
        },

        "SHOW_TIMETABLE": {
            "keywords": {
                "timetable",
                "schedule",
                "routine"
            }
        },

        "FIND_ROOM": {
            "keywords": {
                "room",
                "where",
                "location"
            }
        },

        "FIND_FREE_FACULTY": {
            "keywords": {
                "free",
                "available",
                "vacant"
            }
        },

        "FIND_SUBJECT": {
            "keywords": {
                "subject",
                "course"
            }
        }

    }

    @staticmethod
    def detect(tokens, entities, day_slot):

        words = {token.lower() for token in tokens}

        # -----------------------------------
        # FIND FREE FACULTY
        # -----------------------------------

        if (
            words &
            IntentDetector.INTENT_RULES["FIND_FREE_FACULTY"]["keywords"]
        ):

            if day_slot["day"] or day_slot["slot"]:

                return "FIND_FREE_FACULTY"

        # -----------------------------------
        # FIND TEACHER
        # -----------------------------------

        if (
            words &
            IntentDetector.INTENT_RULES["FIND_TEACHER"]["keywords"]
        ):

            if entities["subjects"]:

                return "FIND_TEACHER"

        # -----------------------------------
        # SHOW TIMETABLE
        # -----------------------------------

        if (
            words &
            IntentDetector.INTENT_RULES["SHOW_TIMETABLE"]["keywords"]
        ):

            if (
                entities["teachers"] or
                entities["classes"] or
                entities["groups"]
            ):

                return "SHOW_TIMETABLE"

        # -----------------------------------
        # FIND ROOM
        # -----------------------------------

        if (
            words &
            IntentDetector.INTENT_RULES["FIND_ROOM"]["keywords"]
        ):

            if entities["subjects"]:

                return "FIND_ROOM"

        # -----------------------------------
        # FIND SUBJECT
        # -----------------------------------

        if (
            words &
            IntentDetector.INTENT_RULES["FIND_SUBJECT"]["keywords"]
        ):

            if entities["teachers"]:

                return "FIND_SUBJECT"

        return "UNKNOWN"