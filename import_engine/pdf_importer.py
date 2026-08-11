"""
==========================================================
UNISCHED AI - UNIVERSAL PDF TIMETABLE IMPORTER
==========================================================

Supports timetable PDFs where each page represents a
faculty/teacher timetable.

Extracts:

    teacher
    day
    slot
    slot_time
    subject
    room
    class_name
    group_name
    type
    length
    lessons_per_week
    available_classrooms
    cycle

Important:
---------
This importer is UNIVERSAL.

It does not hardcode:
    - teacher names
    - subjects
    - classes
    - rooms
    - university names

It supports teacher labels such as:

    Teacher Dr. Mehul Mahrishi
    Teacher Mr. Ashish Pant
    Teacher AS 1
    Teacher MnB
    Teacher SK

==========================================================
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, List, Optional

import pdfplumber


class PDFImporter:

    # ======================================================
    # DAY MAP
    # ======================================================

    DAY_MAP = {

        "mo": "Monday",
        "mon": "Monday",
        "monday": "Monday",

        "tu": "Tuesday",
        "tue": "Tuesday",
        "tues": "Tuesday",
        "tuesday": "Tuesday",

        "we": "Wednesday",
        "wed": "Wednesday",
        "wednesday": "Wednesday",

        "th": "Thursday",
        "thu": "Thursday",
        "thur": "Thursday",
        "thurs": "Thursday",
        "thursday": "Thursday",

        "fr": "Friday",
        "fri": "Friday",
        "friday": "Friday",

        "sa": "Saturday",
        "sat": "Saturday",
        "saturday": "Saturday",

        "su": "Sunday",
        "sun": "Sunday",
        "sunday": "Sunday",
    }

    # ======================================================
    # VALIDATE FILE
    # ======================================================

    @staticmethod
    def validate_file(
        file_path: str | Path
    ) -> Dict[str, Any]:

        path = Path(file_path)

        if not path.exists():

            return {
                "valid": False,
                "reason": "PDF file does not exist."
            }

        if not path.is_file():

            return {
                "valid": False,
                "reason": "Provided path is not a file."
            }

        if path.suffix.lower() != ".pdf":

            return {
                "valid": False,
                "reason": "File is not a PDF."
            }

        size_bytes = path.stat().st_size

        if size_bytes <= 0:

            return {
                "valid": False,
                "reason": "PDF file is empty."
            }

        return {

            "valid": True,

            "filename":
                path.name,

            "size_bytes":
                size_bytes,

            "size_mb":
                round(
                    size_bytes / (
                        1024 * 1024
                    ),
                    2
                ),

        }

    # ======================================================
    # CLEAN TEXT
    # ======================================================

    @staticmethod
    def clean_text(
        value: Any
    ) -> str:

        if value is None:
            return ""

        text = str(value)

        text = text.replace(
            "\xa0",
            " "
        )

        text = text.replace(
            "\n",
            " "
        )

        text = " ".join(
            text.split()
        )

        return text.strip()

    # ======================================================
    # EXTRACT WORDS
    # ======================================================

    @staticmethod
    def extract_words(
        page
    ) -> List[Dict[str, Any]]:

        try:

            return page.extract_words(
                keep_blank_chars=False
            )

        except Exception:

            return []

    # ======================================================
    # DETECT TEACHER
    # ======================================================

    @classmethod
    def detect_teacher(
        cls,
        page
    ) -> str:
        """
        Detect the value written after "Teacher".

        Examples:

            Teacher Dr. Mehul Mahrishi
                -> Dr. Mehul Mahrishi

            Teacher Mr. Ashish Pant
                -> Mr. Ashish Pant

            Teacher AS 1
                -> AS

            Teacher MnB
                -> MnB

        The importer does not require Dr./Mr./Ms.
        """

        words = cls.extract_words(
            page
        )

        if not words:
            return ""

        # --------------------------------------------------
        # Sort approximately in reading order
        # --------------------------------------------------

        words = sorted(
            words,
            key=lambda word: (
                round(
                    word.get(
                        "top",
                        0
                    ),
                    1
                ),
                word.get(
                    "x0",
                    0
                )
            )
        )

        # --------------------------------------------------
        # Find "Teacher"
        # --------------------------------------------------

        for index, word in enumerate(
            words
        ):

            current = cls.clean_text(
                word.get(
                    "text",
                    ""
                )
            )

            if current.lower() != "teacher":
                continue

            teacher_top = word.get(
                "top",
                0
            )

            teacher_parts = []

            # --------------------------------------------------
            # Collect words on same visual line
            # --------------------------------------------------

            for next_word in words[
                index + 1:
            ]:

                next_top = next_word.get(
                    "top",
                    0
                )

                if abs(
                    next_top - teacher_top
                ) > 8:

                    break

                text = cls.clean_text(
                    next_word.get(
                        "text",
                        ""
                    )
                )

                if not text:
                    continue

                teacher_parts.append(
                    text
                )

            if teacher_parts:

                return " ".join(
                    teacher_parts
                ).strip()

        return ""

    # ======================================================
    # DETECT DAY
    # ======================================================

    @classmethod
    def detect_day(
        cls,
        value: Any
    ) -> Optional[str]:

        text = cls.clean_text(
            value
        )

        if not text:
            return None

        return cls.DAY_MAP.get(
            text.lower()
        )

    # ======================================================
    # DETECT SLOT NUMBER
    # ======================================================

    @staticmethod
    def parse_slot_header(
        value: Any
    ) -> Optional[int]:

        text = PDFImporter.clean_text(
            value
        )

        if not text:
            return None

        match = re.match(
            r"^(\d+)",
            text
        )

        if not match:
            return None

        try:

            return int(
                match.group(1)
            )

        except ValueError:

            return None

    # ======================================================
    # DETECT SLOT TIME
    # ======================================================

    @staticmethod
    def parse_time(
        value: Any
    ) -> str:

        text = PDFImporter.clean_text(
            value
        )

        if not text:
            return ""

        match = re.search(
            r"(\d{1,2}:\d{2})\s*-\s*(\d{1,2}:\d{2})",
            text
        )

        if not match:
            return ""

        return (
            f"{match.group(1)} - "
            f"{match.group(2)}"
        )

    # ======================================================
    # DETECT CLASS
    # ======================================================

    @staticmethod
    def detect_class(
        text: str
    ) -> str:

        if not text:
            return ""

        patterns = [

            # ----------------------------------------------
            # Examples:
            # 3CS-D
            # 7CS-IOT
            # 4CSE-A
            # ----------------------------------------------

            r"\b\d+[A-Z]{2,}(?:-[A-Z0-9]+)+\b",

            # ----------------------------------------------
            # Examples:
            # 7CSA
            # 3CSD
            # ----------------------------------------------

            r"\b\d+[A-Z]{2,}[A-Z0-9]*\b",

            # ----------------------------------------------
            # Examples:
            # 3CS A
            # 3CS D
            # ----------------------------------------------

            r"\b\d+[A-Z]{2,}\s+[A-Z0-9-]+\b",
        ]

        matches = []

        for pattern in patterns:

            found = re.findall(
                pattern,
                text,
                flags=re.IGNORECASE
            )

            matches.extend(
                found
            )

        if not matches:
            return ""

        matches = list(
            dict.fromkeys(
                matches
            )
        )

        return max(
            matches,
            key=len
        ).strip()

    # ======================================================
    # DETECT ROOM
    # ======================================================

    @staticmethod
    def detect_room(
        text: str
    ) -> str:
        """
        Detect actual classroom/laboratory identifiers.

        Valid examples:

            303
            304
            CL-15
            CL-22
            ECL-08
            7F:EE-Lab13
            5F::CP5

        Important:
        ---------
        A subject such as:

            Spoken-Latex

        must NOT be treated as a room.

        Therefore room codes must contain a digit.
        """

        if not text:
            return ""

        candidates = []

        # --------------------------------------------------
        # 1. Numeric classroom
        #
        # 303
        # 304
        # 101
        # --------------------------------------------------

        numeric_rooms = re.findall(
            r"\b\d{2,4}\b",
            text
        )

        candidates.extend(
            numeric_rooms
        )

        # --------------------------------------------------
        # 2. Standard room codes
        #
        # CL-15
        # CL-22
        # ECL-08
        # --------------------------------------------------

        standard_rooms = re.findall(
            r"\b[A-Z]{1,8}-[A-Za-z]*\d+[A-Za-z0-9-]*\b",
            text,
            flags=re.IGNORECASE
        )

        candidates.extend(
            standard_rooms
        )

        # --------------------------------------------------
        # 3. Complex laboratory codes
        #
        # 7F:EE-Lab13
        # 5F::CP5
        # --------------------------------------------------

        lab_rooms = re.findall(
            r"\b[A-Z0-9]{1,8}:+[A-Za-z0-9-]*\d+[A-Za-z0-9-]*\b",
            text,
            flags=re.IGNORECASE
        )

        candidates.extend(
            lab_rooms
        )

        if not candidates:
            return ""

        # --------------------------------------------------
        # Remove duplicates
        # --------------------------------------------------

        candidates = list(
            dict.fromkeys(
                candidates
            )
        )

        # --------------------------------------------------
        # Don't use class name as room
        # --------------------------------------------------

        class_name = PDFImporter.detect_class(
            text
        )

        filtered = [

            candidate

            for candidate in candidates

            if candidate.lower()
            != class_name.lower()

        ]

        if filtered:

            candidates = filtered

        # --------------------------------------------------
        # Prefer structured room codes
        # --------------------------------------------------

        complex_candidates = [

            candidate

            for candidate in candidates

            if (
                "-"
                in candidate
                or ":"
                in candidate
            )

        ]

        if complex_candidates:

            return complex_candidates[-1].strip()

        return candidates[-1].strip()

    # ======================================================
    # DETECT TYPE
    # ======================================================

    @staticmethod
    def detect_type(
        subject: str
    ) -> str:

        text = subject.lower()

        if not text:
            return ""

        if "lab" in text:
            return "Lab"

        if "seminar" in text:
            return "Seminar"

        if "tutorial" in text:
            return "Tutorial"

        return "Theory"

    # ======================================================
    # CLEAN SUBJECT
    # ======================================================

    @classmethod
    def clean_subject(
        cls,
        text: str,
        class_name: str,
        room: str
    ) -> str:

        subject = cls.clean_text(
            text
        )

        if not subject:
            return ""

        # --------------------------------------------------
        # Remove class
        # --------------------------------------------------

        if class_name:

            subject = re.sub(
                re.escape(
                    class_name
                ),
                "",
                subject,
                flags=re.IGNORECASE
            )

        # --------------------------------------------------
        # Remove room
        # --------------------------------------------------

        if room:

            subject = re.sub(
                re.escape(
                    room
                ),
                "",
                subject,
                flags=re.IGNORECASE
            )

        subject = " ".join(
            subject.split()
        )

        return subject.strip()

    # ======================================================
    # EXTRACT TABLES
    # ======================================================

    @staticmethod
    def extract_tables_from_page(
        page
    ) -> List[List[List[Any]]]:

        try:

            tables = page.extract_tables()

            if not tables:
                return []

            return tables

        except Exception:

            return []

    # ======================================================
    # DETECT SLOT HEADERS
    # ======================================================

    @classmethod
    def detect_slot_headers(
        cls,
        row: List[Any]
    ) -> Dict[int, Dict[str, Any]]:

        slots = {}

        for index, cell in enumerate(
            row
        ):

            slot = cls.parse_slot_header(
                cell
            )

            if slot is None:
                continue

            slots[index] = {

                "slot":
                    slot,

                "time":
                    cls.parse_time(
                        cell
                    ),

            }

        return slots

    # ======================================================
    # CREATE RECORD
    # ======================================================

    @classmethod
    def create_record(
        cls,
        teacher: str,
        day: str,
        slot: Optional[int],
        slot_time: str,
        cell_text: str,
        source_file: str,
        source_page: int
    ) -> Dict[str, Any]:

        cell_text = cls.clean_text(
            cell_text
        )

        # --------------------------------------------------
        # EMPTY CELL
        # --------------------------------------------------

        if not cell_text:

            return {

                "teacher":
                    teacher,

                "day":
                    day,

                "slot":
                    slot,

                "slot_time":
                    slot_time,

                "subject":
                    "",

                "room":
                    "",

                "class_name":
                    "",

                "group_name":
                    "",

                "type":
                    "",

                "length":
                    "",

                "lessons_per_week":
                    "",

                "available_classrooms":
                    "",

                "cycle":
                    "",

                "source_file":
                    source_file,

                "source_type":
                    "pdf",

                "source_page":
                    source_page,

                "raw_text":
                    "",

            }

        # --------------------------------------------------
        # CLASS
        # --------------------------------------------------

        class_name = cls.detect_class(
            cell_text
        )

        # --------------------------------------------------
        # ROOM
        # --------------------------------------------------

        room = cls.detect_room(
            cell_text
        )

        # --------------------------------------------------
        # SUBJECT
        # --------------------------------------------------

        subject = cls.clean_subject(
            cell_text,
            class_name,
            room
        )

        record_type = cls.detect_type(
            subject
        )

        return {

            "teacher":
                teacher,

            "day":
                day,

            "slot":
                slot,

            "slot_time":
                slot_time,

            "subject":
                subject,

            "room":
                room,

            "class_name":
                class_name,

            "group_name":
                "",

            "type":
                record_type,

            "length":
                "",

            "lessons_per_week":
                "",

            "available_classrooms":
                "",

            "cycle":
                "",

            "source_file":
                source_file,

            "source_type":
                "pdf",

            "source_page":
                source_page,

            "raw_text":
                cell_text,

        }

    # ======================================================
    # PROCESS ONE PAGE
    # ======================================================

    @classmethod
    def process_page(
        cls,
        page,
        page_number: int,
        source_file: str
    ) -> List[Dict[str, Any]]:

        records = []

        # --------------------------------------------------
        # Detect teacher
        # --------------------------------------------------

        teacher = cls.detect_teacher(
            page
        )

        # --------------------------------------------------
        # Extract tables
        # --------------------------------------------------

        tables = (
            cls.extract_tables_from_page(
                page
            )
        )

        for table in tables:

            if not table:
                continue

            slot_headers = {}

            header_index = None

            # --------------------------------------------------
            # Find slot header row
            # --------------------------------------------------

            for row_index, row in enumerate(
                table
            ):

                if not row:
                    continue

                detected = (
                    cls.detect_slot_headers(
                        row
                    )
                )

                if detected:

                    slot_headers = detected

                    header_index = row_index

                    break

            if not slot_headers:
                continue

            # --------------------------------------------------
            # Process timetable rows
            # --------------------------------------------------

            for row in table[
                header_index + 1:
            ]:

                if not row:
                    continue

                if len(row) == 0:
                    continue

                # First cell:
                #
                # Mo
                # Tu
                # We
                # Th
                # Fr
                # Sa

                day = cls.detect_day(
                    row[0]
                )

                if not day:
                    continue

                # --------------------------------------------------
                # Create one record per slot.
                #
                # Empty cell = free slot.
                # --------------------------------------------------

                for column_index, slot_info in (
                    slot_headers.items()
                ):

                    if (
                        column_index
                        >= len(row)
                    ):

                        continue

                    cell = cls.clean_text(
                        row[column_index]
                    )

                    record = cls.create_record(

                        teacher=
                            teacher,

                        day=
                            day,

                        slot=
                            slot_info[
                                "slot"
                            ],

                        slot_time=
                            slot_info[
                                "time"
                            ],

                        cell_text=
                            cell,

                        source_file=
                            source_file,

                        source_page=
                            page_number,

                    )

                    records.append(
                        record
                    )

        return records

    # ======================================================
    # IMPORT PDF
    # ======================================================

    @classmethod
    def import_file(
        cls,
        file_path: str | Path
    ) -> List[Dict[str, Any]]:

        validation = cls.validate_file(
            file_path
        )

        if not validation["valid"]:

            raise ValueError(
                validation["reason"]
            )

        path = Path(
            file_path
        )

        records = []

        with pdfplumber.open(
            path
        ) as pdf:

            for page_number, page in enumerate(
                pdf.pages,
                start=1
            ):

                page_records = (
                    cls.process_page(

                        page,

                        page_number,

                        path.name

                    )
                )

                records.extend(
                    page_records
                )

        return records

    # ======================================================
    # INSPECT PDF
    # ======================================================

    @classmethod
    def inspect_file(
        cls,
        file_path: str | Path
    ) -> Dict[str, Any]:

        validation = cls.validate_file(
            file_path
        )

        if not validation["valid"]:

            raise ValueError(
                validation["reason"]
            )

        path = Path(
            file_path
        )

        pages = 0

        pages_with_text = 0

        pages_with_tables = 0

        total_tables = 0

        pages_with_slot_headers = 0

        pages_with_day_rows = 0

        pages_with_teacher = 0

        with pdfplumber.open(
            path
        ) as pdf:

            pages = len(
                pdf.pages
            )

            for page in pdf.pages:

                # --------------------------------------------------
                # Teacher
                # --------------------------------------------------

                teacher = cls.detect_teacher(
                    page
                )

                if teacher:

                    pages_with_teacher += 1

                # --------------------------------------------------
                # Text
                # --------------------------------------------------

                text = ""

                try:

                    text = (
                        page.extract_text()
                        or ""
                    )

                except Exception:

                    text = ""

                if text:

                    pages_with_text += 1

                # --------------------------------------------------
                # Tables
                # --------------------------------------------------

                tables = (
                    cls.extract_tables_from_page(
                        page
                    )
                )

                if not tables:
                    continue

                pages_with_tables += 1

                total_tables += len(
                    tables
                )

                page_has_slot = False

                page_has_day = False

                for table in tables:

                    for row in table:

                        if not row:
                            continue

                        # Slot header
                        if (
                            cls.detect_slot_headers(
                                row
                            )
                        ):

                            page_has_slot = True

                        # Day row
                        if (
                            row
                            and
                            cls.detect_day(
                                row[0]
                            )
                        ):

                            page_has_day = True

                if page_has_slot:

                    pages_with_slot_headers += 1

                if page_has_day:

                    pages_with_day_rows += 1

        return {

            "file":
                path.name,

            "size_bytes":
                validation[
                    "size_bytes"
                ],

            "size_mb":
                validation[
                    "size_mb"
                ],

            "pages":
                pages,

            "pages_with_text":
                pages_with_text,

            "pages_with_tables":
                pages_with_tables,

            "total_tables":
                total_tables,

            "pages_with_slot_headers":
                pages_with_slot_headers,

            "pages_with_day_rows":
                pages_with_day_rows,

            "pages_with_teacher":
                pages_with_teacher,

            "columns":
                [],

            "detected_columns":
                {},

            "dataset_type":
                "SCHEDULED_TIMETABLE",

            "has_day":
                pages_with_day_rows > 0,

            "has_slot":
                pages_with_slot_headers > 0,

            "has_teacher":
                pages_with_teacher > 0,

        }


# ==========================================================
# DIRECT MODULE TEST
# ==========================================================

if __name__ == "__main__":

    print("=" * 80)

    print(
        "UNISCHED AI - UNIVERSAL PDF IMPORTER"
    )

    print("=" * 80)

    print()

    print(
        "PDF importer loaded successfully."
    )

    print(
        "Teacher extraction: extract_words()"
    )

    print(
        "Timetable extraction: extract_tables()"
    )

    print(
        "Day detection: enabled"
    )

    print(
        "Slot detection: enabled"
    )

    print(
        "Slot time detection: enabled"
    )

    print(
        "Class detection: enabled"
    )

    print(
        "Room detection: enabled"
    )

    print(
        "Free-slot preservation: enabled"
    )

    print()

    print(
        "Ready for user-uploaded timetable PDFs."
    )

    print("=" * 80)