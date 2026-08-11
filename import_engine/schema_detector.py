"""
==========================================================
UniSched AI - Universal Schema Detector
==========================================================

Purpose
-------
Detect the meaning of columns in user-uploaded datasets.

The user may upload files from different universities
with different column names.

Examples:

    teacher
    faculty
    instructor
    professor

can all represent:

    TEACHER

Similarly:

    subject
    course
    course name
    paper

can represent:

    SUBJECT

IMPORTANT
---------
This module does NOT depend on a particular university
or a particular timetable file.
==========================================================
"""

from __future__ import annotations

from typing import Dict, List, Any


class SchemaDetector:

    # ==================================================
    # UNIVERSAL FIELD DEFINITIONS
    # ==================================================

    FIELD_ALIASES = {

        "teacher": {

            "teacher",
            "teacher name",
            "faculty",
            "faculty name",
            "faculty member",
            "instructor",
            "instructor name",
            "professor",
            "professor name",
            "staff",
            "staff name",
        },

        "subject": {

            "subject",
            "subject name",
            "course",
            "course name",
            "course_name",
            "paper",
            "paper name",
            "module",
        },

        "class_name": {

            "class",
            "class name",
            "class_name",
            "classname",
            "section",
            "section name",
            "batch",
            "batch name",
            "program",
        },

        "group_name": {

            "group",
            "group name",
            "group_name",
            "student group",
            "lab group",
            "tutorial group",
            "division",
        },

        "room": {

            "room",
            "room name",
            "room_name",
            "classroom",
            "classroom name",
            "classrooms",
            "location",
            "venue",
            "lab",
            "lab room",
        },

        "day": {

            "day",
            "day name",
            "weekday",
            "week day",
            "date",
        },

        "slot": {

            "slot",
            "slot number",
            "time slot",
            "period",
            "period number",
            "lecture period",
            "class period",
        },

        "type": {

            "type",
            "class type",
            "lecture type",
            "session type",
            "activity type",
        },

        "length": {

            "length",
            "duration",
            "class duration",
            "period length",
        },

        "lessons_per_week": {

            "lessons/week",
            "lessons per week",
            "lessons_week",
            "weekly lessons",
            "classes per week",
            "periods per week",
            "hours per week",
        },

        "available_classrooms": {

            "available classrooms",
            "available rooms",
            "available room",
            "available_classrooms",
            "possible rooms",
            "allowed rooms",
        },

        "cycle": {

            "cycle",
            "week cycle",
            "schedule cycle",
            "weeks",
            "week",
        },
    }

    # ==================================================
    # NORMALIZE COLUMN NAME
    # ==================================================

    @staticmethod
    def normalize_column(
        column: Any
    ) -> str:

        if column is None:

            return ""

        text = str(
            column
        ).strip().lower()

        # Replace separators

        text = (
            text
            .replace("_", " ")
            .replace("-", " ")
            .replace("/", " ")
        )

        # Remove duplicate spaces

        text = " ".join(
            text.split()
        )

        return text

    # ==================================================
    # DETECT ONE COLUMN
    # ==================================================

    @classmethod
    def detect_column(
        cls,
        column: Any
    ) -> Dict[str, Any]:
        """
        Detect the semantic meaning of one column.
        """

        normalized = cls.normalize_column(
            column
        )

        # ----------------------------------------------
        # Exact alias match
        # ----------------------------------------------

        for field_name, aliases in (
            cls.FIELD_ALIASES.items()
        ):

            normalized_aliases = {

                cls.normalize_column(alias)

                for alias in aliases

            }

            if normalized in normalized_aliases:

                return {

                    "field":
                        field_name,

                    "confidence":
                        100.0,

                    "matched_by":
                        "exact",

                }

        # ----------------------------------------------
        # Partial matching
        # ----------------------------------------------

        for field_name, aliases in (
            cls.FIELD_ALIASES.items()
        ):

            normalized_aliases = [

                cls.normalize_column(alias)

                for alias in aliases

            ]

            for alias in normalized_aliases:

                if (
                    alias
                    and (
                        alias in normalized
                        or
                        normalized in alias
                    )
                ):

                    return {

                        "field":
                            field_name,

                        "confidence":
                            85.0,

                        "matched_by":
                            "partial",

                    }

        # ----------------------------------------------
        # Unknown
        # ----------------------------------------------

        return {

            "field": None,

            "confidence": 0.0,

            "matched_by": None,

        }

    # ==================================================
    # DETECT COMPLETE SCHEMA
    # ==================================================

    @classmethod
    def detect(
        cls,
        columns: List[Any]
    ) -> Dict[str, Any]:
        """
        Detect the semantic meaning of all columns.
        """

        detected = {}

        unknown = []

        for column in columns:

            result = cls.detect_column(
                column
            )

            field = result["field"]

            if field is None:

                unknown.append(
                    str(column)
                )

                continue

            detected[
                str(column)
            ] = {

                "field":
                    field,

                "confidence":
                    result[
                        "confidence"
                    ],

                "matched_by":
                    result[
                        "matched_by"
                    ],

            }

        return {

            "detected":
                detected,

            "unknown":
                unknown,

        }

    # ==================================================
    # REVERSE MAP
    # ==================================================

    @classmethod
    def get_universal_mapping(
        cls,
        columns: List[Any]
    ) -> Dict[str, str]:
        """
        Return:

            original column
                ↓
            universal field

        Example:

            {
                "teacher": "teacher",
                "faculty": "teacher",
                "course": "subject"
            }
        """

        mapping = {}

        for column in columns:

            result = cls.detect_column(
                column
            )

            if result["field"]:

                mapping[
                    str(column)
                ] = result["field"]

        return mapping

    # ==================================================
    # REQUIRED FIELD CHECK
    # ==================================================

    @classmethod
    def check_required_fields(
        cls,
        columns: List[Any]
    ) -> Dict[str, Any]:
        """
        Determine which important universal fields
        are present.

        We deliberately do NOT require every field.

        A dataset may legitimately contain only:

            Teacher
            Subject
            Class

        and still be useful.
        """

        mapping = cls.get_universal_mapping(
            columns
        )

        universal_fields = set(
            mapping.values()
        )

        important_fields = {

            "teacher",
            "subject",
            "class_name",
            "group_name",
            "room",
            "day",
            "slot",

        }

        available = (
            universal_fields
            & important_fields
        )

        missing = (
            important_fields
            - universal_fields
        )

        return {

            "available":
                sorted(available),

            "missing":
                sorted(missing),

        }

    # ==================================================
    # DATASET CAPABILITIES
    # ==================================================

    @classmethod
    def detect_capabilities(
        cls,
        columns: List[Any]
    ) -> Dict[str, bool]:
        """
        Determine what kinds of questions the dataset
        may potentially support.

        This is important because the chatbot must not
        answer questions requiring information that the
        uploaded dataset doesn't contain.
        """

        mapping = cls.get_universal_mapping(
            columns
        )

        fields = set(
            mapping.values()
        )

        return {

            "teacher_queries":
                "teacher" in fields,

            "subject_queries":
                "subject" in fields,

            "class_queries":
                "class_name" in fields,

            "group_queries":
                "group_name" in fields,

            "room_queries":
                "room" in fields,

            "day_queries":
                "day" in fields,

            "slot_queries":
                "slot" in fields,

            "availability_queries":
                (
                    "teacher" in fields
                    and
                    "day" in fields
                    and
                    "slot" in fields
                ),

        }


# ======================================================
# DIRECT TEST
# ======================================================

if __name__ == "__main__":

    print("=" * 80)

    print(
        "UNISCHED AI - SCHEMA DETECTOR TEST"
    )

    print("=" * 80)

    test_columns = [

        "teacher",
        "subject",
        "class",
        "group",
        "classrooms",
        "lessons/week",
        "available classrooms",
        "cycle",

    ]

    print(
        "\nINPUT COLUMNS"
    )

    print("-" * 80)

    for column in test_columns:

        print(
            column
        )

    result = (
        SchemaDetector.detect(
            test_columns
        )
    )

    print(
        "\nDETECTED SCHEMA"
    )

    print("-" * 80)

    for column, information in (
        result["detected"].items()
    ):

        print(
            f"{column} "
            f"-> "
            f"{information['field']} "
            f"({information['confidence']}%)"
        )

    print(
        "\nUNKNOWN COLUMNS"
    )

    print("-" * 80)

    for column in result["unknown"]:

        print(
            column
        )

    capabilities = (
        SchemaDetector.detect_capabilities(
            test_columns
        )
    )

    print(
        "\nDATASET CAPABILITIES"
    )

    print("-" * 80)

    for capability, supported in (
        capabilities.items()
    ):

        print(
            f"{capability}: "
            f"{supported}"
        )

    print(
        "\nSchema detector test completed."
    )