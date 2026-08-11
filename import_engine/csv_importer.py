"""
==========================================================
UniSched AI - Universal CSV Importer
==========================================================

Purpose
-------
Import user-uploaded CSV datasets and convert them into
the same universal record format used by ExcelImporter.

The importer attempts to recognize common timetable/data
columns such as:

    teacher
    faculty
    subject
    course
    class
    section
    group
    room
    classroom
    day
    slot
    period
    type
    etc.

IMPORTANT
---------
No university-specific data is hardcoded.

The user supplies the CSV file at runtime.
==========================================================
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

import pandas as pd


class CSVImporter:

    # ======================================================
    # COLUMN ALIASES
    # ======================================================

    COLUMN_ALIASES = {

        "class_name": {
            "class",
            "class name",
            "classname",
            "class_name",
            "section",
            "section name",
            "batch",
            "batch name",
            "program",
        },

        "teacher": {
            "teacher",
            "teacher name",
            "faculty",
            "faculty name",
            "instructor",
            "instructor name",
            "professor",
            "professor name",
            "staff",
            "staff name",
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

        "room": {
            "room",
            "room name",
            "room_name",
            "classroom",
            "classroom name",
            "classrooms",
            "location",
            "venue",
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

    # ======================================================
    # NORMALIZE COLUMN
    # ======================================================

    @staticmethod
    def _normalize_column(
        column: Any
    ) -> str:

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

    # ======================================================
    # CLEAN COLUMNS
    # ======================================================

    @classmethod
    def _clean_columns(
        cls,
        dataframe: pd.DataFrame
    ) -> pd.DataFrame:

        dataframe = dataframe.copy()

        dataframe.columns = [
            cls._normalize_column(column)
            for column in dataframe.columns
        ]

        return dataframe

    # ======================================================
    # DETECT COLUMNS
    # ======================================================

    @classmethod
    def _detect_columns(
        cls,
        columns
    ) -> Dict[str, str]:

        normalized_columns = {
            cls._normalize_column(column): column
            for column in columns
        }

        mapping = {}

        for standard_name, aliases in (
            cls.COLUMN_ALIASES.items()
        ):

            for alias in aliases:

                normalized_alias = (
                    cls._normalize_column(alias)
                )

                if normalized_alias in normalized_columns:

                    mapping[standard_name] = (
                        normalized_columns[
                            normalized_alias
                        ]
                    )

                    break

        return mapping

    # ======================================================
    # READ CSV
    # ======================================================

    @staticmethod
    def _read_csv(
        file_path: str | Path
    ) -> pd.DataFrame:
        """
        Read CSV while attempting common encodings.

        This is useful because CSV files may come from
        Excel, Windows applications, or other systems.
        """

        encodings = [
            "utf-8",
            "utf-8-sig",
            "cp1252",
            "latin1",
        ]

        last_error = None

        for encoding in encodings:

            try:

                return pd.read_csv(
                    file_path,
                    encoding=encoding
                )

            except UnicodeDecodeError as exc:

                last_error = exc

        if last_error:

            raise last_error

        return pd.read_csv(
            file_path
        )

    # ======================================================
    # VALUE
    # ======================================================

    @staticmethod
    def _value(
        row: pd.Series,
        mapping: Dict[str, str],
        key: str,
        default: str = ""
    ) -> str:

        column = mapping.get(key)

        if not column:
            return default

        value = row.get(column)

        if pd.isna(value):
            return default

        return str(value).strip()

    # ======================================================
    # PARSE SLOT
    # ======================================================

    @staticmethod
    def _parse_slot(
        value: str
    ):

        if not value:
            return None

        try:

            number = float(value)

            if number.is_integer():
                return int(number)

        except (
            ValueError,
            TypeError
        ):

            pass

        return None

    # ======================================================
    # VALID RECORD
    # ======================================================

    @staticmethod
    def _is_valid_record(
        record: Dict[str, Any]
    ) -> bool:
        """
        Reject completely empty/header-like rows.

        A class name alone is not enough to create a
        timetable assignment.
        """

        return any([
            bool(record.get("teacher")),
            bool(record.get("subject")),
            bool(record.get("group_name")),
            bool(record.get("room")),
            bool(record.get("day")),
            record.get("slot") is not None,
        ])

    # ======================================================
    # CONVERT ROW
    # ======================================================

    @classmethod
    def _convert_row(
        cls,
        row: pd.Series,
        mapping: Dict[str, str],
        source_file: str
    ) -> Dict[str, Any]:

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

        slot = cls._parse_slot(
            slot_text
        )

        # ----------------------------------------------
        # Infer type only if missing
        # ----------------------------------------------

        if not class_type:

            if "lab" in subject.lower():

                class_type = "Lab"

            else:

                class_type = "Theory"

        return {

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
                "csv",
        }

    # ======================================================
    # IMPORT FILE
    # ======================================================

    @classmethod
    def import_file(
        cls,
        file_path: str | Path
    ) -> List[Dict[str, Any]]:

        file_path = Path(file_path)

        if not file_path.exists():

            raise FileNotFoundError(
                f"CSV file not found: {file_path}"
            )

        dataframe = cls._read_csv(
            file_path
        )

        dataframe = cls._clean_columns(
            dataframe
        )

        mapping = cls._detect_columns(
            dataframe.columns
        )

        dataframe = cls._forward_fill_class(
            dataframe,
            mapping
        )

        records = []

        for _, row in dataframe.iterrows():

            record = cls._convert_row(
                row,
                mapping,
                file_path.name
            )

            if not cls._is_valid_record(
                record
            ):
                continue

            records.append(record)

        return records

    # ======================================================
    # FORWARD FILL CLASS
    # ======================================================

    @classmethod
    def _forward_fill_class(
        cls,
        dataframe: pd.DataFrame,
        mapping: Dict[str, str]
    ) -> pd.DataFrame:

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

    # ======================================================
    # INSPECT FILE
    # ======================================================

    @classmethod
    def inspect_file(
        cls,
        file_path: str | Path
    ) -> Dict[str, Any]:

        file_path = Path(file_path)

        if not file_path.exists():

            raise FileNotFoundError(
                f"CSV file not found: {file_path}"
            )

        dataframe = cls._read_csv(
            file_path
        )

        dataframe = cls._clean_columns(
            dataframe
        )

        mapping = cls._detect_columns(
            dataframe.columns
        )

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


# ==========================================================
# DIRECT TEST
# ==========================================================

if __name__ == "__main__":

    print("=" * 80)

    print(
        "UNISCHED AI - CSV IMPORTER"
    )

    print("=" * 80)

    print(
        "CSV importer loaded successfully."
    )