import re


class GroupParser:

    @staticmethod
    def extract(text):

        match = re.search(
            r"\bGroup\s+(\d+)\b",
            text,
            re.IGNORECASE
        )

        if not match:
            return "", text

        group = f"Group {match.group(1)}"

        remaining = re.sub(
            r"\bGroup\s+\d+\b",
            "",
            text,
            flags=re.IGNORECASE
        )

        remaining = " ".join(remaining.split())

        return group, remaining