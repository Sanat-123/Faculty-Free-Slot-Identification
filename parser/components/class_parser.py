import re


class ClassParser:

    PATTERNS = [

        # 3CS-DS-A
        r"\b\d+[A-Z]+(?:-[A-Z]+)+\b",

        # 3CSC
        r"\b\d+CS[A-Z]\b",

    ]

    @staticmethod
    def extract(text: str):

        for pattern in ClassParser.PATTERNS:

            match = re.search(pattern, text, re.IGNORECASE)

            if match:

                class_name = match.group()

                cleaned = re.sub(
        re.escape(class_name),
          "",
            text,
          flags=re.IGNORECASE
        ).strip()

                return class_name, cleaned

        return "", text