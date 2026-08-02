import re


class TeacherSubjectExtractor:

    @staticmethod
    def extract(question):

        result = {
            "subject": "",
            "class": "",
            "group": "",
            "day": "",
            "slot": ""
        }

        # ---------------- CLASS ----------------

        m = re.search(
            r"\b\d+[A-Z]+(?:-[A-Z]+)?-[A-Z]\b",
            question,
            re.IGNORECASE
        )

        if m:
            result["class"] = m.group()

            question = question.replace(
                m.group(),
                ""
            )

        # ---------------- GROUP ----------------

        m = re.search(
            r"Group\s+\d+",
            question,
            re.IGNORECASE
        )

        if m:

            result["group"] = m.group()

            question = question.replace(
                m.group(),
                ""
            )

        # ---------------- DAY ----------------

        m = re.search(
            r"Monday|Tuesday|Wednesday|Thursday|Friday|Saturday",
            question,
            re.IGNORECASE
        )

        if m:

            result["day"] = m.group().title()

            question = question.replace(
                m.group(),
                ""
            )

        # ---------------- SLOT ----------------

        m = re.search(
            r"Slot\s+(\d+)",
            question,
            re.IGNORECASE
        )

        if m:

            result["slot"] = int(m.group(1))

            question = question.replace(
                m.group(),
                ""
            )

        # ---------------- SUBJECT ----------------

        patterns = [

            r"Who teaches",
            r"Teacher of",
            r"Faculty for",
            r"In",
            r"\?"
        ]

        for p in patterns:

            question = re.sub(
                p,
                "",
                question,
                flags=re.IGNORECASE
            )

        result["subject"] = " ".join(
            question.split()
        )

        return result