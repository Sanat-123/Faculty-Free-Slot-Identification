"""
==========================================================
UniSched AI
Universal Excel Importer
==========================================================

Supports:

1. Scheduled timetable Excel files
   - Day
   - Slot
   - Teacher
   - Subject
   - Room
   - Class
   - Group

2. Class-contract Excel files
   - Class
   - Teacher
   - Group
   - Subject
   - Length
   - Lessons/week
   - Available classrooms
   - Cycle
   - Classrooms

The importer converts different Excel formats into a
common UniSched record structure.

Universal normalization is delegated to:
    import_engine.universal_normalizer.UniversalNormalizer

The importer does NOT contain university-specific,
semester-specific, faculty-specific, or dataset-specific
rules.
==========================================================
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

import pandas as pd

from import_engine.universal_normalizer import UniversalNormalizer


class ExcelImporter:
    """
    Universal Excel importer for UniSched AI.
    """

    # ==================================================
    # COLUMN ALIASES
    # ==================================================

    COLUMN_ALIASES = {

        "class_name": {
            "class",
            "class name",
            "classname",
            "class_name",
            "section",
        },

        "teacher": {
            "teacher",
            "faculty",
            "faculty name",
            "teacher name",
            "instructor",
            "professor",
            "professor name",
            "faculty member",
            "faculty_member",
        },

        "group_name": {
            "group",
            "group name",
            "group_name",
            "batch",
            "batch name",
            "division",
        },

        "subject": {
            "subject",
            "course",
            "course name",
            "course_name",
            "paper",
            "module",
        },

        "length": {
            "length",
            "duration",
        },

        "lessons_per_week": {
            "lessons/week",
            "lessons per week",
            "lessons_week",
            "weekly lessons",
            "weekly classes",
        },

        "available_classrooms": {
            "available classrooms",
            "available rooms",
            "available room",
            "available_classrooms",
        },

        "cycle": {
            "cycle",
            "week cycle",
        },

        "room": {
            "room",
            "classroom",
            "classrooms",
            "room name",
            "room_name",
            "location",
            "venue",
        },

        "day": {
            "day",
            "weekday",
            "week day",
        },

        "slot": {
            "slot",
            "period",
            "period number",
            "time slot",
            "slot number",
            "period no",
            "period no.",
        },

        "type": {
            "type",
            "class type",
            "lecture type",
            "session type",
        },
    }

    # ==================================================
    # IMPORT FILE
    # ==================================================

    @classmethod
    def import_file(
        cls,
        file_path: str | Path
    ) -> List[Dict[str, Any]]:
        """
        Read an Excel file and convert it into
        UniSched's common record format.
        """

        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(
                f"Excel file not found: {file_path}"
            )

        if file_path.suffix.lower() not in {
            ".xlsx",
            ".xls",
            ".xlsm",
        }:
            raise ValueError(
                f"Unsupported Excel format: "
                f"{file_path.suffix}"
            )

        # ----------------------------------------------
        # Read Excel
        # ----------------------------------------------

        dataframe = pd.read_excel(
            file_path,
            sheet_name=0
        )

        # ----------------------------------------------
        # Clean column names
        # ----------------------------------------------

        dataframe = cls._clean_columns(
            dataframe
        )

        # ----------------------------------------------
        # Detect semantic columns
        # ----------------------------------------------

        mapping = cls._detect_columns(
            dataframe.columns
        )

        # ----------------------------------------------
        # Forward-fill class names
        #
        # Example:
        #
        # 3CS A
        # assignment
        # assignment
        #
        # The class name belongs to the following
        # assignment rows until the next class.
        # ----------------------------------------------

        dataframe = cls._forward_fill_class(
            dataframe,
            mapping
        )

        records: List[Dict[str, Any]] = []

        for _, row in dataframe.iterrows():

            record = cls._convert_row(
                row,
                mapping,
                file_path.name
            )

            # ------------------------------------------
            # Ignore class-header / summary rows
            # ------------------------------------------

            if not cls._is_valid_record(
                record
            ):
                continue

            records.append(record)

        return records

    # ==================================================
    # NORMALIZE COLUMN NAME
    # ==================================================

    @staticmethod
    def _normalize_column_name(
        column: Any
    ) -> str:
        """
        Convert column names into a standard form.
        """

        if column is None:
            return ""

        text = str(column).strip().lower()

        text = (
            text
            .replace("_", " ")
            .replace("-", " ")
            .replace("/", " ")
        )

        text = " ".join(
            text.split()
        )

        return text

    # ==================================================
    # CLEAN COLUMNS
    # ==================================================

    @classmethod
    def _clean_columns(
        cls,
        dataframe: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Normalize all Excel column names.
        """

        dataframe = dataframe.copy()

        dataframe.columns = [
            cls._normalize_column_name(
                column
            )
            for column in dataframe.columns
        ]

        return dataframe

    # ==================================================
    # DETECT COLUMNS
    # ==================================================

    @classmethod
    def _detect_columns(
        cls,
        columns
    ) -> Dict[str, str]:
        """
        Detect semantic columns from different
        possible column names.
        """

        normalized_columns = {
            cls._normalize_column_name(column): column
            for column in columns
        }

        mapping: Dict[str, str] = {}

        for standard_name, aliases in (
            cls.COLUMN_ALIASES.items()
        ):

            for alias in aliases:

                normalized_alias = (
                    cls._normalize_column_name(
                        alias
                    )
                )

                if (
                    normalized_alias
                    in normalized_columns
                ):

                    mapping[standard_name] = (
                        normalized_columns[
                            normalized_alias
                        ]
                    )

                    break

        return mapping

    # ==================================================
    # FORWARD FILL CLASS
    # ==================================================

    @classmethod
    def _forward_fill_class(
        cls,
        dataframe: pd.DataFrame,
        mapping: Dict[str, str]
    ) -> pd.DataFrame:
        """
        Carry the latest class name down to
        following assignment rows.
        """

        dataframe = dataframe.copy()

        class_column = mapping.get(
            "class_name"
        )

        if not class_column:
            return dataframe

        dataframe[class_column] = (
            dataframe[class_column]
            .ffill()
        )

        return dataframe

    # ==================================================
    # GET SAFE VALUE
    # ==================================================

    @staticmethod
    def _value(
        row: pd.Series,
        mapping: Dict[str, str],
        key: str,
        default: str = ""
    ) -> str:
        """
        Safely retrieve a value from a row.
        """

        column = mapping.get(key)

        if not column:
            return default

        value = row.get(column)

        if pd.isna(value):
            return default

        return str(value).strip()

    # ==================================================
    # CONVERT ROW
    # ==================================================

    @classmethod
    def _convert_row(
        cls,
        row: pd.Series,
        mapping: Dict[str, str],
        source_file: str
    ) -> Dict[str, Any]:
        """
        Convert one Excel row into a universal
        UniSched record.
        """

        teacher = cls._value(
            row,
            mapping,
            "teacher"
        )

        subject = cls._value(
            row,
            mapping,
            "subject"
        )

        class_name = cls._value(
            row,
            mapping,
            "class_name"
        )

        group_name = cls._value(
            row,
            mapping,
            "group_name"
        )

        room = cls._value(
            row,
            mapping,
            "room"
        )

        day = cls._value(
            row,
            mapping,
            "day"
        )

        slot_text = cls._value(
            row,
            mapping,
            "slot"
        )

        length = cls._value(
            row,
            mapping,
            "length"
        )

        lessons_per_week = cls._value(
            row,
            mapping,
            "lessons_per_week"
        )

        available_classrooms = cls._value(
            row,
            mapping,
            "available_classrooms"
        )

        cycle = cls._value(
            row,
            mapping,
            "cycle"
        )

        class_type = cls._value(
            row,
            mapping,
            "type"
        )

        # ----------------------------------------------
        # Convert slot using UNIVERSAL NORMALIZER
        # ----------------------------------------------

        slot = cls._parse_slot(
            slot_text
        )

        # ----------------------------------------------
        # Infer type only when source doesn't provide it
        #
        # This is a generic heuristic, not tied to a
        # particular university.
        # ----------------------------------------------

        if not class_type:

            if "lab" in subject.lower():
                class_type = "Lab"
            else:
                class_type = "Theory"

        # ----------------------------------------------
        # Universal record
        # ----------------------------------------------

        record = {
            "teacher": teacher,
            "day": day,
            "slot": slot,
            "subject": subject,
            "room": room,
            "class_name": class_name,
            "group_name": group_name,
            "type": class_type,
            "length": length,
            "lessons_per_week":
                lessons_per_week,
            "available_classrooms":
                available_classrooms,
            "cycle": cycle,
            "source_file":
                source_file,
            "source_type":
                "excel",
        }

        # ----------------------------------------------
        # Apply universal normalization
        # ----------------------------------------------

        return UniversalNormalizer.normalize_record(
            record
        )

    # ==================================================
    # SLOT PARSER
    # ==================================================

    @staticmethod
    def _parse_slot(
        value: Any
    ):
        """
        Delegate slot interpretation to the universal
        normalizer.

        Examples:

            3          -> 3
            3.0        -> 3
            "3"        -> 3
            "3.0"      -> 3
            "Slot 3"   -> 3
            "Period 3" -> 3
            "P3"       -> 3
        """

        return UniversalNormalizer.normalize_slot(
            value
        )

    # ==================================================
    # VALID RECORD
    # ==================================================

    @staticmethod
    def _is_valid_record(
        record: Dict[str, Any]
    ) -> bool:
        """
        Determine whether a row represents a real
        timetable/class assignment.

        A class header such as:

            3CS A

        should NOT become a timetable record.

        A real assignment such as:

            Dr. Niketa Sharma
            DE Lab
            Group 2

        should become a record.
        """

        # ------------------------------------------------
        # A real assignment must contain at least one
        # meaningful field OTHER THAN class_name.
        # ------------------------------------------------

        return any([
            bool(record.get("teacher")),
            bool(record.get("subject")),
            bool(record.get("group_name")),
            bool(record.get("room")),
            bool(record.get("day")),
            record.get("slot") is not None,
        ])

    # ==================================================
    # INSPECT FILE
    # ==================================================

    @classmethod
    def inspect_file(
        cls,
        file_path: str | Path
    ) -> Dict[str, Any]:
        """
        Inspect an Excel file without importing records.

        Useful for the Upload Manager.
        """

        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(
                f"Excel file not found: {file_path}"
            )

        if file_path.suffix.lower() not in {
            ".xlsx",
            ".xls",
            ".xlsm",
        }:
            raise ValueError(
                f"Unsupported Excel format: "
                f"{file_path.suffix}"
            )

        dataframe = pd.read_excel(
            file_path,
            sheet_name=0
        )

        dataframe = cls._clean_columns(
            dataframe
        )

        mapping = cls._detect_columns(
            dataframe.columns
        )

        # ------------------------------------------------
        # Determine dataset type
        # ------------------------------------------------

        has_day = (
            "day" in mapping
        )

        has_slot = (
            "slot" in mapping
        )

        if has_day and has_slot:

            dataset_type = (
                "SCHEDULED_TIMETABLE"
            )

        else:

            dataset_type = (
                "CLASS_CONTRACT"
            )

        return {
            "file":
                file_path.name,

            "rows":
                len(dataframe),

            "columns":
                list(dataframe.columns),

            "detected_columns":
                mapping,

            "dataset_type":
                dataset_type,

            "has_day":
                has_day,

            "has_slot":
                has_slot,
        }


# ======================================================
# DIRECT TEST
# ======================================================

if __name__ == "__main__":

    print("=" * 80)

    print(
        "UniSched AI - Universal Excel Importer"
    )

    print("=" * 80)

    print(
        "This module is intended to be imported "
        "by the Import Manager."
    )