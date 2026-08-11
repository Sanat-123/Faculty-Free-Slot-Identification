from pathlib import Path
from collections import Counter, defaultdict

from import_engine.import_manager import ImportManager
from data_engine.canonical_event_matcher import CanonicalEventMatcher


print("=" * 80)
print("UNISCHED AI - CANONICAL EVENT DIAGNOSTICS")
print("=" * 80)


FILES = [

    Path(r"data\Facultywise TT 20 sep.pdf"),

    Path(r"data\classwise TT 27 sep.pdf"),

    Path(r"data\Location wise TT 27 sep 2025.pdf"),

    Path(r"data\timetable.xlsx"),

    Path(r"data\test_timetable.csv"),

]


manager = ImportManager()

all_records = []


# ==========================================================
# IMPORT
# ==========================================================

for file_path in FILES:

    print()
    print(
        "IMPORTING:",
        file_path.name
    )

    result = manager.import_file(
        file_path
    )

    if result["success"]:

        print(
            "SUCCESS:",
            result["record_count"]
        )

        all_records.extend(
            result["records"]
        )

    else:

        print(
            "FAILED:",
            result.get("error")
        )


# ==========================================================
# MATCH
# ==========================================================

matcher = CanonicalEventMatcher()

events = matcher.match(
    all_records
)

unmatched = matcher.get_unmatched()


summary = matcher.summary()


print()
print("=" * 80)
print("OVERALL SUMMARY")
print("=" * 80)

print(
    "Input records:",
    summary["input_records"]
)

print(
    "Canonical events:",
    summary["canonical_events"]
)

print(
    "Unmatched records:",
    summary["unmatched_records"]
)

print(
    "Multi-source events:",
    summary["multi_source_events"]
)

print(
    "Conflict events:",
    summary["conflict_events"]
)


# ==========================================================
# SOURCE-WISE ANALYSIS
# ==========================================================

print()
print("=" * 80)
print("UNMATCHED RECORDS BY SOURCE")
print("=" * 80)


source_counts = Counter()

for record in unmatched:

    source = record.get(
        "source_file",
        "UNKNOWN"
    )

    source_counts[
        source
    ] += 1


for source, count in (
    source_counts.most_common()
):

    print(
        f"{count:5d}  {source}"
    )


# ==========================================================
# FIELD COMPLETENESS
# ==========================================================

print()
print("=" * 80)
print("UNMATCHED FIELD COMPLETENESS")
print("=" * 80)


field_names = [

    "teacher",
    "day",
    "slot",
    "slot_time",
    "subject",
    "room",
    "class_name",
    "group_name",

]


for field in field_names:

    present = 0
    missing = 0

    for record in unmatched:

        value = record.get(
            field
        )

        if value is None:

            missing += 1

        elif str(value).strip() == "":

            missing += 1

        else:

            present += 1

    print(
        f"{field:20s} "
        f"present={present:5d} "
        f"missing={missing:5d}"
    )


# ==========================================================
# RECORD TYPE ANALYSIS
# ==========================================================

print()
print("=" * 80)
print("UNMATCHED RECORD TYPES")
print("=" * 80)


def has_value(
    record,
    field
):

    value = record.get(
        field
    )

    return (
        value is not None
        and str(value).strip() != ""
    )


for source in source_counts:

    source_records = [

        record

        for record in unmatched

        if record.get(
            "source_file"
        ) == source

    ]

    scheduled = 0
    empty = 0
    useful = 0

    for record in source_records:

        has_day = has_value(
            record,
            "day"
        )

        has_slot = has_value(
            record,
            "slot"
        )

        has_content = any(

            has_value(
                record,
                field
            )

            for field in [

                "teacher",
                "subject",
                "room",
                "class_name",

            ]

        )

        if has_day and has_slot:

            scheduled += 1

        if (
            has_day
            and has_slot
            and not has_content
        ):

            empty += 1

        if has_content:

            useful += 1

    print()
    print(
        source
    )

    print(
        "  scheduled:",
        scheduled
    )

    print(
        "  empty:",
        empty
    )

    print(
        "  useful:",
        useful
    )


# ==========================================================
# SHOW SAMPLE UNMATCHED RECORDS
# ==========================================================

print()
print("=" * 80)
print("FIRST 30 UNMATCHED USEFUL RECORDS")
print("=" * 80)


shown = 0

for record in unmatched:

    useful = any(

        has_value(
            record,
            field
        )

        for field in [

            "teacher",
            "subject",
            "room",
            "class_name",

        ]

    )

    if not useful:

        continue

    shown += 1

    print()
    print(
        f"RECORD {shown}"
    )

    print(
        "Source:",
        record.get(
            "source_file",
            ""
        )
    )

    print(
        "Teacher:",
        record.get(
            "teacher",
            ""
        )
    )

    print(
        "Day:",
        record.get(
            "day",
            ""
        )
    )

    print(
        "Slot:",
        record.get(
            "slot",
            ""
        )
    )

    print(
        "Slot time:",
        record.get(
            "slot_time",
            ""
        )
    )

    print(
        "Subject:",
        record.get(
            "subject",
            ""
        )
    )

    print(
        "Room:",
        record.get(
            "room",
            ""
        )
    )

    print(
        "Class:",
        record.get(
            "class_name",
            ""
        )
    )

    if shown >= 30:

        break


print()
print("=" * 80)
print("DIAGNOSTICS COMPLETE")
print("=" * 80)