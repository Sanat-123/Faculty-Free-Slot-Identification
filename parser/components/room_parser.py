import re

from config.locations import KNOWN_LOCATIONS


class RoomParser:

    @staticmethod
    def extract(text: str):

        text = text.strip()


         # ---------- CL-xx ----------
        match = re.search(r"\bCL-\d+\b", text, re.IGNORECASE)

        if match:

            room = match.group()

            cleaned = text.replace(room, "").strip()

            return room, cleaned
        

        

        # ---------- Known Locations ----------
        for location in sorted(KNOWN_LOCATIONS, key=len, reverse=True):

            if location.lower() in text.lower():

                cleaned = re.sub(
                    re.escape(location),
                    "",
                    text,
                    flags=re.IGNORECASE
                ).strip()

                return location, cleaned

        

        # ---------- Numeric Room ----------
        match = re.search(r"\b\d{3}\b", text)

        if match:

            room = match.group()

            cleaned = text.replace(room, "").strip()

            return room, cleaned

        return "", text