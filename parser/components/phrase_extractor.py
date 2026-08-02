import re

from config.locations import KNOWN_LOCATIONS


class PhraseExtractor:

    @staticmethod
    def extract(text: str):

        phrases = []

        text = re.sub(r"\s+", " ", text).strip()

        # -------- Known Locations --------
        for location in sorted(KNOWN_LOCATIONS, key=len, reverse=True):

            pattern = re.escape(location)

            if re.search(pattern, text, re.IGNORECASE):

                phrases.append(location)

                text = re.sub(
                    pattern,
                    "",
                    text,
                    flags=re.IGNORECASE
                ).strip()

        # -------- Group --------
        group = re.search(r"Group\s+\d+", text, re.IGNORECASE)

        if group:

            phrases.append(group.group())

            text = re.sub(
                r"Group\s+\d+",
                "",
                text,
                flags=re.IGNORECASE
            ).strip()

        # -------- Remaining Words --------
        phrases.extend(text.split())

        return phrases