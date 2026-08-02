import re


class Normalizer:
    """
    Normalization utilities.

    normalize()
        -> Canonical formatting
           (used for displaying/storing)

    normalize_for_match()
        -> Lowercase search normalization
           (used only for searching)
    """

    @staticmethod
    def normalize(text: str) -> str:

        if not text:
            return ""

        text = text.strip()
        text = re.sub(r"\s+", " ", text)

        # ---------- Class ----------
        class_pattern = re.fullmatch(
            r"(\d+)\s*([a-z]+)\s*([a-z]+)\s*([a-z])",
            text,
            re.IGNORECASE
        )

        if class_pattern:

            return (
                f"{class_pattern.group(1)}"
                f"{class_pattern.group(2).upper()}-"
                f"{class_pattern.group(3).upper()}-"
                f"{class_pattern.group(4).upper()}"
            )

        # ---------- Group ----------
        group = re.fullmatch(
            r"group\s*(\d+)",
            text,
            re.IGNORECASE
        )

        if group:

            return f"Group {group.group(1)}"

        # ---------- Room ----------
        text = re.sub(
            r"\b(CL|LAB|R|B)\s*-?\s*(\d+)\b",
            lambda m: f"{m.group(1).upper()}-{m.group(2)}",
            text,
            flags=re.IGNORECASE
        )

        return text

    @staticmethod
    def normalize_for_match(text: str) -> str:
        """
        Search normalization.

        Used ONLY inside UniversalMatcher.
        """

        if not text:
            return ""

        text = Normalizer.normalize(text)

        text = text.lower()

        text = re.sub(r"[^a-z0-9]+", " ", text)

        text = re.sub(r"\s+", " ", text).strip()

        return text