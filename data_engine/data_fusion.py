"""
==========================================================
UNISCHED AI - SAFE DATA FUSION ENGINE
==========================================================

Combines records from:

    Facultywise PDF
    Classwise PDF
    Location-wise PDF
    Excel
    CSV

Important design rules:

1. Empty timetable cells are NOT events.
2. Contract datasets without day/slot are NOT merged with
   scheduled timetable events.
3. Records are only considered duplicates when enough
   meaningful information is available.
4. Missing fields do NOT become wildcard duplicates.
5. Original source information is preserved.

==========================================================
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any, Dict, List, Tuple


class DataFusionEngine:

    # ======================================================
    # CONSTRUCTOR
    # ======================================================

    def __init__(self):

        self.records: List[
            Dict[str, Any]
        ] = []

        self.event_groups = defaultdict(list)

        self.ignored_empty_records = []

    # ======================================================
    # TEXT NORMALIZATION
    # ======================================================

    @staticmethod
    def normalize_text(
        value: Any
    ) -> str:

        if value is None:
            return ""

        text = str(value).strip().lower()

        return " ".join(
            text.split()
        )

    # ======================================================
    # DAY NORMALIZATION
    # ======================================================

    @staticmethod
    def normalize_day(
        value: Any
    ) -> str:

        value = (
            DataFusionEngine
            .normalize_text(value)
        )

        mapping = {

            "mo": "monday",
            "mon": "monday",
            "monday": "monday",

            "tu": "tuesday",
            "tue": "tuesday",
            "tues": "tuesday",
            "tuesday": "tuesday",

            "we": "wednesday",
            "wed": "wednesday",
            "wednesday": "wednesday",

            "th": "thursday",
            "thu": "thursday",
            "thur": "thursday",
            "thursday": "thursday",

            "fr": "friday",
            "fri": "friday",
            "friday": "friday",

            "sa": "saturday",
            "sat": "saturday",
            "saturday": "saturday",

            "su": "sunday",
            "sun": "sunday",
            "sunday": "sunday",

        }

        return mapping.get(
            value,
            value
        )

    # ======================================================
    # SLOT NORMALIZATION
    # ======================================================

    @staticmethod
    def normalize_slot(
        value: Any
    ):

        if value in (
            None,
            ""
        ):

            return None

        try:

            return int(
                float(value)
            )

        except (
            ValueError,
            TypeError
        ):

            return str(
                value
            ).strip()

    # ======================================================
    # GET FIELD
    # ======================================================

    @staticmethod
    def field(
        record: Dict[str, Any],
        name: str
    ) -> str:

        return DataFusionEngine.normalize_text(
            record.get(
                name,
                ""
            )
        )

    # ======================================================
    # DETERMINE WHETHER RECORD HAS DAY/SLOT
    # ======================================================

    def is_scheduled_record(
        self,
        record: Dict[str, Any]
    ) -> bool:

        day = self.normalize_day(
            record.get(
                "day"
            )
        )

        slot = self.normalize_slot(
            record.get(
                "slot"
            )
        )

        return bool(
            day and slot is not None
        )

    # ======================================================
    # DETERMINE WHETHER RECORD IS EMPTY
    # ======================================================

    def is_empty_schedule_cell(
        self,
        record: Dict[str, Any]
    ) -> bool:

        if not self.is_scheduled_record(
            record
        ):

            return False

        important_fields = [

            "teacher",
            "subject",
            "room",
            "class_name",
            "group_name",

        ]

        for field in important_fields:

            value = self.field(
                record,
                field
            )

            if value:

                return False

        return True

    # ======================================================
    # DETERMINE WHETHER RECORD HAS USEFUL CONTENT
    # ======================================================

    def has_meaningful_content(
        self,
        record: Dict[str, Any]
    ) -> bool:

        fields = [

            "teacher",
            "subject",
            "room",
            "class_name",
            "group_name",
            "day",
            "slot",

        ]

        return any(

            self.field(
                record,
                field
            )

            for field in fields

        )

    # ======================================================
    # RECORD TYPE
    # ======================================================

    def record_type(
        self,
        record: Dict[str, Any]
    ) -> str:

        if self.is_empty_schedule_cell(
            record
        ):

            return "EMPTY_SCHEDULE_CELL"

        if self.is_scheduled_record(
            record
        ):

            return "SCHEDULED_EVENT"

        return "CONTRACT_RECORD"

    # ======================================================
    # SAFE EVENT KEY
    # ======================================================

    def event_key(
        self,
        record: Dict[str, Any]
    ) -> Tuple | None:

        """
        Create a duplicate key ONLY when sufficient
        information exists.

        We never create a key consisting only of:

            day + slot

        because that would merge unrelated timetable cells.
        """

        # --------------------------------------------------
        # Ignore empty schedule cells
        # --------------------------------------------------

        if self.is_empty_schedule_cell(
            record
        ):

            return None

        # --------------------------------------------------
        # Scheduled timetable event
        # --------------------------------------------------

        if self.is_scheduled_record(
            record
        ):

            day = self.normalize_day(
                record.get(
                    "day"
                )
            )

            slot = self.normalize_slot(
                record.get(
                    "slot"
                )
            )

            teacher = self.field(
                record,
                "teacher"
            )

            subject = self.field(
                record,
                "subject"
            )

            room = self.field(
                record,
                "room"
            )

            class_name = self.field(
                record,
                "class_name"
            )

            group_name = self.field(
                record,
                "group_name"
            )

            # --------------------------------------------------
            # Need enough identity information.
            # --------------------------------------------------

            meaningful = [

                teacher,
                subject,
                room,
                class_name,
                group_name,

            ]

            meaningful_count = sum(
                bool(value)
                for value in meaningful
            )

            if meaningful_count < 2:

                return None

            # --------------------------------------------------
            # Primary scheduled key
            # --------------------------------------------------

            return (

                "SCHEDULED",

                day,

                slot,

                teacher,

                subject,

                room,

                class_name,

                group_name,

            )

        # --------------------------------------------------
        # Contract record
        # --------------------------------------------------

        teacher = self.field(
            record,
            "teacher"
        )

        subject = self.field(
            record,
            "subject"
        )

        room = self.field(
            record,
            "room"
        )

        class_name = self.field(
            record,
            "class_name"
        )

        group_name = self.field(
            record,
            "group_name"
        )

        # --------------------------------------------------
        # Contract records must have useful identity.
        # --------------------------------------------------

        meaningful = [

            teacher,
            subject,
            room,
            class_name,
            group_name,

        ]

        meaningful_count = sum(
            bool(value)
            for value in meaningful
        )

        if meaningful_count < 2:

            return None

        return (

            "CONTRACT",

            teacher,

            subject,

            room,

            class_name,

            group_name,

        )

    # ======================================================
    # ADD RECORD
    # ======================================================

    def add_record(
        self,
        record: Dict[str, Any]
    ):

        if not isinstance(
            record,
            dict
        ):

            return

        # --------------------------------------------------
        # Completely empty record
        # --------------------------------------------------

        if not self.has_meaningful_content(
            record
        ):

            self.ignored_empty_records.append(
                record
            )

            return

        # --------------------------------------------------
        # Empty timetable cell
        # --------------------------------------------------

        if self.is_empty_schedule_cell(
            record
        ):

            self.ignored_empty_records.append(
                record
            )

            return

        # --------------------------------------------------
        # Store original record
        # --------------------------------------------------

        self.records.append(
            record
        )

        # --------------------------------------------------
        # Generate safe key
        # --------------------------------------------------

        key = self.event_key(
            record
        )

        # --------------------------------------------------
        # If not enough information for duplicate
        # detection, keep it as an independent record.
        # --------------------------------------------------

        if key is None:

            return

        self.event_groups[
            key
        ].append(
            record
        )

    # ======================================================
    # ADD MANY RECORDS
    # ======================================================

    def add_records(
        self,
        records: List[
            Dict[str, Any]
        ]
    ):

        for record in records:

            self.add_record(
                record
            )

    # ======================================================
    # RAW RECORD COUNT
    # ======================================================

    def raw_record_count(
        self
    ) -> int:

        return len(
            self.records
        )

    # ======================================================
    # EMPTY RECORD COUNT
    # ======================================================

    def empty_record_count(
        self
    ) -> int:

        return len(
            self.ignored_empty_records
        )

    # ======================================================
    # DUPLICATE GROUPS
    # ======================================================

    def duplicate_groups(
        self
    ):

        return {

            key: records

            for key, records
            in self.event_groups.items()

            if len(records) > 1

        }

    # ======================================================
    # DUPLICATE RECORD COUNT
    # ======================================================

    def duplicate_record_count(
        self
    ) -> int:

        total = 0

        for records in (
            self.duplicate_groups()
            .values()
        ):

            total += (
                len(records) - 1
            )

        return total

    # ======================================================
    # UNIQUE EVENT COUNT
    # ======================================================

    def unique_event_count(
        self
    ) -> int:

        return len(
            self.event_groups
        )

    # ======================================================
    # EVENT GROUPS
    # ======================================================

    def get_groups(
        self
    ):

        return dict(
            self.event_groups
        )

    # ======================================================
    # SOURCE FILES
    # ======================================================

    def sources_for_records(
        self,
        records
    ) -> List[str]:

        sources = set()

        for record in records:

            source = str(
                record.get(
                    "source_file",
                    ""
                )
            ).strip()

            if source:

                sources.add(
                    source
                )

        return sorted(
            sources
        )

    # ======================================================
    # BUILD FUSED DATASET
    # ======================================================

    def build_fused_dataset(
        self
    ) -> List[
        Dict[str, Any]
    ]:

        fused = []

        # --------------------------------------------------
        # Add one representative per duplicate group.
        # --------------------------------------------------

        for key, records in (
            self.event_groups.items()
        ):

            representative = dict(
                records[0]
            )

            representative[
                "source_files"
            ] = self.sources_for_records(
                records
            )

            representative[
                "source_count"
            ] = len(
                records
            )

            representative[
                "duplicate_sources"
            ] = len(
                records
            ) > 1

            fused.append(
                representative
            )

        # --------------------------------------------------
        # Add records that could not safely be grouped.
        # --------------------------------------------------

        grouped_ids = set()

        for records in (
            self.event_groups.values()
        ):

            for record in records:

                grouped_ids.add(
                    id(record)
                )

        for record in self.records:

            if id(record) not in grouped_ids:

                copy = dict(
                    record
                )

                copy[
                    "source_files"
                ] = [

                    record.get(
                        "source_file",
                        ""
                    )

                ]

                copy[
                    "source_count"
                ] = 1

                copy[
                    "duplicate_sources"
                ] = False

                fused.append(
                    copy
                )

        return fused

    # ======================================================
    # SUMMARY
    # ======================================================

    def summary(
        self
    ) -> Dict[str, Any]:

        duplicates = (
            self.duplicate_groups()
        )

        return {

            "raw_records":
                self.raw_record_count(),

            "empty_schedule_cells":
                self.empty_record_count(),

            "unique_events":
                self.unique_event_count(),

            "duplicate_records":
                self.duplicate_record_count(),

            "duplicate_groups":
                len(duplicates),

            "total_groups":
                len(
                    self.event_groups
                ),

        }


# ==========================================================
# DIRECT TEST
# ==========================================================

if __name__ == "__main__":

    print("=" * 70)

    print(
        "UNISCHED AI - SAFE DATA FUSION ENGINE"
    )

    print("=" * 70)

    engine = DataFusionEngine()

    # ------------------------------------------------------
    # Same real event from two sources
    # ------------------------------------------------------

    engine.add_records([

        {

            "teacher":
                "Dr. Mehul Mahrishi",

            "day":
                "Monday",

            "slot":
                3,

            "subject":
                "OS III",

            "room":
                "303",

            "class_name":
                "3CS-D",

            "source_file":
                "Facultywise TT 20 sep.pdf",

        },

        {

            "teacher":
                "Dr. Mehul Mahrishi",

            "day":
                "Mo",

            "slot":
                3,

            "subject":
                "OS III",

            "room":
                "303",

            "class_name":
                "3CS-D",

            "source_file":
                "Another timetable.pdf",

        },

        # --------------------------------------------------
        # Empty cells
        # --------------------------------------------------

        {

            "teacher":
                "",

            "day":
                "Wednesday",

            "slot":
                4,

            "subject":
                "",

            "room":
                "",

            "class_name":
                "",

            "source_file":
                "classwise TT 27 sep.pdf",

        },

        {

            "teacher":
                "",

            "day":
                "Wednesday",

            "slot":
                4,

            "subject":
                "",

            "room":
                "",

            "class_name":
                "",

            "source_file":
                "Location wise TT 27 sep 2025.pdf",

        },

    ])

    summary = engine.summary()

    print()

    print(
        "Raw records:",
        summary[
            "raw_records"
        ]
    )

    print(
        "Empty schedule cells:",
        summary[
            "empty_schedule_cells"
        ]
    )

    print(
        "Unique events:",
        summary[
            "unique_events"
        ]
    )

    print(
        "Duplicate records:",
        summary[
            "duplicate_records"
        ]
    )

    print(
        "Duplicate groups:",
        summary[
            "duplicate_groups"
        ]
    )

    print()

    print(
        "Expected:"
    )

    print(
        "  Raw records: 2"
    )

    print(
        "  Empty schedule cells: 2"
    )

    print(
        "  Unique events: 1"
    )

    print(
        "  Duplicate records: 1"
    )

    print(
        "  Duplicate groups: 1"
    )

    print()

    print(
        "Safe Data Fusion Engine loaded successfully."
    )

    print("=" * 70)