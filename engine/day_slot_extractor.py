import re


class DaySlotExtractor:

    DAYS = {
        "monday": "Monday",
        "tuesday": "Tuesday",
        "wednesday": "Wednesday",
        "thursday": "Thursday",
        "friday": "Friday",
        "saturday": "Saturday",
        "sunday": "Sunday",

        "mon": "Monday",
        "tue": "Tuesday",
        "wed": "Wednesday",
        "thu": "Thursday",
        "fri": "Friday",
        "sat": "Saturday",
        "sun": "Sunday"
    }

    SCHEDULING_WORDS = {
        "slot",
        "period",
        "lecture",
        "class",
        "available",
        "free"
    }

    @staticmethod
    def extract(tokens):

        day = None
        slot = None
        remaining = []

        i = 0

        while i < len(tokens):

            token = tokens[i].lower()

            # -----------------------------
            # Day
            # -----------------------------

            if token in DaySlotExtractor.DAYS:

                day = DaySlotExtractor.DAYS[token]
                i += 1
                continue

            # -----------------------------
            # Slot 3
            # -----------------------------

            if token in {"slot", "period"}:

                if i + 1 < len(tokens):

                    nxt = tokens[i + 1]

                    if nxt.isdigit():

                        slot = int(nxt)

                        i += 2
                        continue

            # -----------------------------
            # Standalone number
            # Only if scheduling context exists
            # -----------------------------

            if re.fullmatch(r"\d+", token):

                previous = tokens[i - 1].lower() if i > 0 else ""
                next_word = tokens[i + 1].lower() if i + 1 < len(tokens) else ""

                if (
                    previous in DaySlotExtractor.SCHEDULING_WORDS
                    or next_word in DaySlotExtractor.SCHEDULING_WORDS
                    or day is not None
                ):

                    value = int(token)

                    if 1 <= value <= 10:

                        slot = value
                        i += 1
                        continue

            remaining.append(tokens[i])

            i += 1

        return {
            "day": day,
            "slot": slot,
            "remaining_tokens": remaining
        }