"""
UNISCHED AI - Universal Timetable Normalizer

Purpose:
    Normalize common timetable values into a consistent representation
    regardless of whether the source is PDF, Excel, or CSV.

This module intentionally contains NO university-specific names,
semester-specific rules, teacher names, class names, or file names.
"""

import re
from typing import Any, Optional


class UniversalNormalizer:
    """Common normalization utilities for all timetable importers."""

    EMPTY_VALUES = {
        "",
        "-",
        "--",
        "—",
        "_",
        "na",
        "n/a",
        "nan",
        "none",
        "null",
        "nil",
    }

    DAY_ALIASES = {
        "mon": "monday",
        "monday": "monday",

        "tue": "tuesday",
        "tues": "tuesday",
        "tuesday": "tuesday",

        "wed": "wednesday",
        "weds": "wednesday",
        "wednesday": "wednesday",

        "thu": "thursday",
        "thur": "thursday",
        "thurs": "thursday",
        "thursday": "thursday",

        "fri": "friday",
        "friday": "friday",

        "sat": "saturday",
        "saturday": "saturday",

        "sun": "sunday",
        "sunday": "sunday",
    }

    @staticmethod
    def clean_text(value: Any) -> str:
        """
        Convert a value to clean text.

        Examples:
            "  Dr. ABC  " -> "Dr. ABC"
            "Room   203"  -> "Room 203"
        """
        if value is None:
            return ""

        text = str(value).strip()

        if not text:
            return ""

        # Normalize common Unicode whitespace.
        text = re.sub(r"\s+", " ", text)

        return text.strip()

    @classmethod
    def normalize_empty(cls, value: Any) -> str:
        """
        Convert common empty/null representations to "".
        """
        text = cls.clean_text(value)

        if text.lower() in cls.EMPTY_VALUES:
            return ""

        return text

    @classmethod
    def normalize_day(cls, value: Any) -> str:
        """
        Normalize common day representations.

        Examples:
            Monday -> monday
            MON -> monday
            Tue -> tuesday
        """
        text = cls.normalize_empty(value)

        if not text:
            return ""

        key = re.sub(r"[^a-z]", "", text.lower())

        if key in cls.DAY_ALIASES:
            return cls.DAY_ALIASES[key]

        return text.lower()

    @classmethod
    def normalize_slot(cls, value: Any) -> Optional[int]:
        """
        Normalize timetable slot/period representations.

        Supported examples:
            1
            1.0
            "1"
            "1.0"
            "Slot 1"
            "slot 1"
            "Period 1"
            "period 1"
            "P1"
            "p1"

        Returns:
            int slot number or None if no slot can be identified.
        """
        text = cls.normalize_empty(value)

        if not text:
            return None

        # Numeric values.
        if isinstance(value, int):
            return value

        if isinstance(value, float):
            if value.is_integer():
                return int(value)

        # Remove unnecessary whitespace.
        text = text.strip()

        # Simple numeric string: "3" / "3.0"
        match = re.fullmatch(r"(\d+)(?:\.0+)?", text)
        if match:
            return int(match.group(1))

        # Slot / Period / P prefixes.
        match = re.fullmatch(
            r"(?:slot|period|p)\s*[-:_]?\s*(\d+)",
            text,
            flags=re.IGNORECASE,
        )

        if match:
            return int(match.group(1))

        # More permissive fallback:
        # "Period No. 3", "Slot No 3", "P-3"
        match = re.search(
            r"(?:slot|period|period\s*no\.?|slot\s*no\.?|p)"
            r"\s*[-:#.]?\s*(\d+)",
            text,
            flags=re.IGNORECASE,
        )

        if match:
            return int(match.group(1))

        return None

    @classmethod
    def normalize_time(cls, value: Any) -> str:
        """
        Normalize common timetable time-range formatting.

        This method intentionally preserves the actual time values
        instead of making assumptions about a university's slot timings.

        Examples:
            "09:15-10:15"   -> "09:15 - 10:15"
            "09:15 - 10:15" -> "09:15 - 10:15"
            "9:15 to 10:15" -> "9:15 - 10:15"
        """
        text = cls.normalize_empty(value)

        if not text:
            return ""

        # Normalize Unicode dashes.
        text = text.replace("–", "-").replace("—", "-")

        # Normalize "to" between two times.
        text = re.sub(
            r"\s+to\s+",
            " - ",
            text,
            flags=re.IGNORECASE,
        )

        # Normalize spaces around a hyphen when it appears to be
        # a time range.
        time_range = re.fullmatch(
            r"\s*(\d{1,2})[:.](\d{2})\s*-\s*"
            r"(\d{1,2})[:.](\d{2})\s*",
            text,
        )

        if time_range:
            h1, m1, h2, m2 = time_range.groups()
            return f"{int(h1):02d}:{m1} - {int(h2):02d}:{m2}"

        return text

    @classmethod
    def normalize_record(cls, record: dict) -> dict:
        """
        Apply common normalization to a timetable record.

        Unknown fields are preserved.

        This makes the function safe for existing importers because
        it does not delete information supplied by the source parser.
        """
        normalized = dict(record)

        if "teacher" in normalized:
            normalized["teacher"] = cls.normalize_empty(
                normalized["teacher"]
            )

        if "subject" in normalized:
            normalized["subject"] = cls.normalize_empty(
                normalized["subject"]
            )

        if "room" in normalized:
            normalized["room"] = cls.normalize_empty(
                normalized["room"]
            )

        if "class_name" in normalized:
            normalized["class_name"] = cls.normalize_empty(
                normalized["class_name"]
            )

        if "group_name" in normalized:
            normalized["group_name"] = cls.normalize_empty(
                normalized["group_name"]
            )

        if "type" in normalized:
            normalized["type"] = cls.normalize_empty(
                normalized["type"]
            )

        if "day" in normalized:
            normalized["day"] = cls.normalize_day(
                normalized["day"]
            )

        if "slot" in normalized:
            normalized["slot"] = cls.normalize_slot(
                normalized["slot"]
            )

        if "slot_time" in normalized:
            normalized["slot_time"] = cls.normalize_time(
                normalized["slot_time"]
            )

        return normalized