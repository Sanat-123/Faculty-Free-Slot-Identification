"""
==========================================================
UNISCHED AI - UNIVERSAL DATASET MANAGER
==========================================================

Purpose
-------
Combine records imported from:

    PDF
    Excel
    CSV

into one universal dataset.

The dataset manager does NOT assume that every source
contains the same fields.

For example:

PDF may provide:

    teacher
    day
    slot
    subject
    room
    class_name

Excel may provide:

    teacher
    subject
    class_name
    group_name
    lessons_per_week
    room

CSV may provide another combination.

The manager preserves the information that actually
exists in each source.

==========================================================
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, List


class UniversalDataset:

    # ======================================================
    # STANDARD FIELDS
    # ======================================================

    STANDARD_FIELDS = [

        "teacher",

        "day",

        "slot",

        "slot_time",

        "subject",

        "room",

        "class_name",

        "group_name",

        "type",

        "length",

        "lessons_per_week",

        "available_classrooms",

        "cycle",

        "source_file",

        "source_type",

        "source_page",

        "raw_text",

    ]

    # ======================================================
    # CONSTRUCTOR
    # ======================================================

    def __init__(self):

        self.records: List[
            Dict[str, Any]
        ] = []

        self.source_files = set()

    # ======================================================
    # NORMALIZE RECORD
    # ======================================================

    def normalize_record(
        self,
        record: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Convert an imported record into the universal
        internal format.
        """

        normalized = {}

        for field in self.STANDARD_FIELDS:

            value = record.get(
                field,
                ""
            )

            if value is None:

                value = ""

            normalized[field] = value

        # --------------------------------------------------
        # Normalize source metadata
        # --------------------------------------------------

        normalized[
            "source_file"
        ] = str(
            normalized.get(
                "source_file",
                ""
            )
        )

        normalized[
            "source_type"
        ] = str(
            normalized.get(
                "source_type",
                ""
            )
        ).lower()

        # --------------------------------------------------
        # Slot normalization
        # --------------------------------------------------

        slot = normalized.get(
            "slot"
        )

        if slot == "":
            slot = None

        normalized[
            "slot"
        ] = slot

        return normalized

    # ======================================================
    # ADD ONE RECORD
    # ======================================================

    def add_record(
        self,
        record: Dict[str, Any]
    ):

        normalized = self.normalize_record(
            record
        )

        self.records.append(
            normalized
        )

        source_file = normalized.get(
            "source_file"
        )

        if source_file:

            self.source_files.add(
                source_file
            )

    # ======================================================
    # ADD MANY RECORDS
    # ======================================================

    def add_records(
        self,
        records: Iterable[
            Dict[str, Any]
        ]
    ):

        for record in records:

            if not isinstance(
                record,
                dict
            ):

                continue

            self.add_record(
                record
            )

    # ======================================================
    # RECORD COUNT
    # ======================================================

    def count(self) -> int:

        return len(
            self.records
        )

    # ======================================================
    # SOURCE FILE COUNT
    # ======================================================

    def source_count(self) -> int:

        return len(
            self.source_files
        )

    # ======================================================
    # GET SOURCES
    # ======================================================

    def get_sources(self) -> List[str]:

        return sorted(
            self.source_files
        )

    # ======================================================
    # DETECT AVAILABLE FIELDS
    # ======================================================

    def available_fields(
        self
    ) -> List[str]:

        available = []

        for field in self.STANDARD_FIELDS:

            for record in self.records:

                value = record.get(
                    field
                )

                if value not in (
                    "",
                    None
                ):

                    available.append(
                        field
                    )

                    break

        return available

    # ======================================================
    # MISSING FIELDS
    # ======================================================

    def missing_fields(
        self
    ) -> List[str]:

        available = set(
            self.available_fields()
        )

        return [

            field

            for field in self.STANDARD_FIELDS

            if field not in available

        ]

    # ======================================================
    # FILTER RECORDS
    # ======================================================

    def filter(
        self,
        **conditions
    ) -> List[
        Dict[str, Any]
    ]:

        results = []

        for record in self.records:

            matched = True

            for field, expected in (
                conditions.items()
            ):

                actual = record.get(
                    field
                )

                if isinstance(
                    actual,
                    str
                ):

                    if str(
                        actual
                    ).lower() != str(
                        expected
                    ).lower():

                        matched = False

                        break

                else:

                    if actual != expected:

                        matched = False

                        break

            if matched:

                results.append(
                    record
                )

        return results

    # ======================================================
    # FIND FREE RECORDS
    # ======================================================

    def find_free(
        self,
        teacher: str,
        day: str,
        slot: int
    ) -> List[
        Dict[str, Any]
    ]:

        results = []

        for record in self.records:

            record_teacher = str(
                record.get(
                    "teacher",
                    ""
                )
            ).strip().lower()

            record_day = str(
                record.get(
                    "day",
                    ""
                )
            ).strip().lower()

            record_slot = record.get(
                "slot"
            )

            if (
                record_teacher
                != teacher.strip().lower()
            ):

                continue

            if (
                record_day
                != day.strip().lower()
            ):

                continue

            if record_slot != slot:

                continue

            subject = str(
                record.get(
                    "subject",
                    ""
                )
            ).strip()

            # Empty subject means free slot
            if not subject:

                results.append(
                    record
                )

        return results

    # ======================================================
    # FIND BUSY RECORDS
    # ======================================================

    def find_busy(
        self,
        teacher: str,
        day: str,
        slot: int
    ) -> List[
        Dict[str, Any]
    ]:

        results = []

        for record in self.records:

            record_teacher = str(
                record.get(
                    "teacher",
                    ""
                )
            ).strip().lower()

            record_day = str(
                record.get(
                    "day",
                    ""
                )
            ).strip().lower()

            record_slot = record.get(
                "slot"
            )

            if (
                record_teacher
                != teacher.strip().lower()
            ):

                continue

            if (
                record_day
                != day.strip().lower()
            ):

                continue

            if record_slot != slot:

                continue

            subject = str(
                record.get(
                    "subject",
                    ""
                )
            ).strip()

            if subject:

                results.append(
                    record
                )

        return results

    # ======================================================
    # FIND ALL TEACHERS
    # ======================================================

    def get_teachers(
        self
    ) -> List[str]:

        teachers = set()

        for record in self.records:

            teacher = str(
                record.get(
                    "teacher",
                    ""
                )
            ).strip()

            if teacher:

                teachers.add(
                    teacher
                )

        return sorted(
            teachers
        )

    # ======================================================
    # FIND ALL SUBJECTS
    # ======================================================

    def get_subjects(
        self
    ) -> List[str]:

        subjects = set()

        for record in self.records:

            subject = str(
                record.get(
                    "subject",
                    ""
                )
            ).strip()

            if subject:

                subjects.add(
                    subject
                )

        return sorted(
            subjects
        )

    # ======================================================
    # FIND ALL CLASSES
    # ======================================================

    def get_classes(
        self
    ) -> List[str]:

        classes = set()

        for record in self.records:

            class_name = str(
                record.get(
                    "class_name",
                    ""
                )
            ).strip()

            if class_name:

                classes.add(
                    class_name
                )

        return sorted(
            classes
        )

    # ======================================================
    # FIND ALL ROOMS
    # ======================================================

    def get_rooms(
        self
    ) -> List[str]:

        rooms = set()

        for record in self.records:

            room = str(
                record.get(
                    "room",
                    ""
                )
            ).strip()

            if room:

                rooms.add(
                    room
                )

        return sorted(
            rooms
        )

    # ======================================================
    # SUMMARY
    # ======================================================

    def summary(
        self
    ) -> Dict[str, Any]:

        return {

            "record_count":
                self.count(),

            "source_file_count":
                self.source_count(),

            "source_files":
                self.get_sources(),

            "available_fields":
                self.available_fields(),

            "missing_fields":
                self.missing_fields(),

            "teacher_count":
                len(
                    self.get_teachers()
                ),

            "subject_count":
                len(
                    self.get_subjects()
                ),

            "class_count":
                len(
                    self.get_classes()
                ),

            "room_count":
                len(
                    self.get_rooms()
                ),

        }

    # ======================================================
    # CLEAR DATASET
    # ======================================================

    def clear(self):

        self.records.clear()

        self.source_files.clear()

    # ======================================================
    # EXPORT RECORDS
    # ======================================================

    def to_list(
        self
    ) -> List[
        Dict[str, Any]
    ]:

        return list(
            self.records
        )


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    print("=" * 70)

    print(
        "UNISCHED AI - UNIVERSAL DATASET MANAGER"
    )

    print("=" * 70)

    dataset = UniversalDataset()

    dataset.add_records([

        {

            "teacher":
                "Dr. Example",

            "day":
                "Monday",

            "slot":
                1,

            "slot_time":
                "8:15 - 9:15",

            "subject":
                "Operating Systems",

            "room":
                "303",

            "class_name":
                "3CS-D",

            "source_file":
                "example.pdf",

            "source_type":
                "pdf",

        },

        {

            "teacher":
                "Dr. Example",

            "day":
                "Monday",

            "slot":
                2,

            "slot_time":
                "9:15 - 10:15",

            "subject":
                "",

            "room":
                "",

            "class_name":
                "",

            "source_file":
                "example.pdf",

            "source_type":
                "pdf",

        },

    ])

    print()

    print(
        "Records:",
        dataset.count()
    )

    print(
        "Sources:",
        dataset.get_sources()
    )

    print(
        "Teachers:",
        dataset.get_teachers()
    )

    print(
        "Subjects:",
        dataset.get_subjects()
    )

    print(
        "Classes:",
        dataset.get_classes()
    )

    print(
        "Rooms:",
        dataset.get_rooms()
    )

    print()

    print(
        "Available fields:"
    )

    for field in dataset.available_fields():

        print(
            "  ✓",
            field
        )

    print()

    print(
        "Universal dataset manager loaded successfully."
    )

    print("=" * 70)