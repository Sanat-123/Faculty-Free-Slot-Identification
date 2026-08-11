from pathlib import Path

from import_engine.import_manager import ImportManager
from dataset_manager.universal_dataset import UniversalDataset
from data_engine.data_fusion import DataFusionEngine


print("=" * 80)
print("UNISCHED AI - REAL DATA FUSION TEST")
print("=" * 80)


# ==========================================================
# REAL DATASET FILES
# ==========================================================

FILES = [

    Path(
        r"data\Facultywise TT 20 sep.pdf"
    ),

    Path(
        r"data\classwise TT 27 sep.pdf"
    ),

    Path(
        r"data\Location wise TT 27 sep 2025.pdf"
    ),

    Path(
        r"data\timetable.xlsx"
    ),

    Path(
        r"data\test_timetable.csv"
    ),

]


# ==========================================================
# IMPORT MANAGER
# ==========================================================

manager = ImportManager()


# ==========================================================
# UNIVERSAL DATASET
# ==========================================================

dataset = UniversalDataset()


# ==========================================================
# IMPORT ALL FILES
# ==========================================================

for file_path in FILES:

    print()
    print("-" * 80)

    print(
        "IMPORTING:",
        file_path.name
    )

    print("-" * 80)

    if not file_path.exists():

        print(
            "FILE NOT FOUND:",
            file_path
        )

        continue

    result = manager.import_file(
        file_path
    )

    if result["success"]:

        print(
            "SUCCESS"
        )

        print(
            "Type:",
            result["file_type"]
        )

        print(
            "Records:",
            result["record_count"]
        )

        dataset.add_records(
            result["records"]
        )

    else:

        print(
            "FAILED"
        )

        print(
            "Error:",
            result.get(
                "error"
            )
        )


# ==========================================================
# IMPORT SUMMARY
# ==========================================================

print()
print("=" * 80)

print(
    "IMPORT SUMMARY"
)

print("=" * 80)

print(
    "Total imported records:",
    dataset.count()
)

print(
    "Total source files:",
    dataset.source_count()
)


# ==========================================================
# DATA FUSION
# ==========================================================

print()
print("=" * 80)

print(
    "STARTING DATA FUSION"
)

print("=" * 80)


fusion = DataFusionEngine()


fusion.add_records(
    dataset.to_list()
)


# ==========================================================
# FUSION SUMMARY
# ==========================================================

summary = fusion.summary()


print()
print(
    "RAW RECORDS:",
    summary[
        "raw_records"
    ]
)

print(
    "UNIQUE EVENTS:",
    summary[
        "unique_events"
    ]
)

print(
    "DUPLICATE RECORDS:",
    summary[
        "duplicate_records"
    ]
)

print(
    "DUPLICATE GROUPS:",
    summary[
        "duplicate_groups"
    ]
)

print(
    "TOTAL GROUPS:",
    summary[
        "total_groups"
    ]
)


# ==========================================================
# DUPLICATE GROUP DETAILS
# ==========================================================

duplicates = fusion.duplicate_groups()


print()
print("=" * 80)

print(
    "DUPLICATE GROUP ANALYSIS"
)

print("=" * 80)


print(
    "Number of duplicate groups:",
    len(duplicates)
)


# Show only first 10 groups
# to keep terminal output manageable.

for index, (
    key,
    records
) in enumerate(
    duplicates.items()
):

    if index >= 10:

        break

    print()
    print(
        f"GROUP {index + 1}"
    )

    print(
        "-" * 60
    )

    print(
        "Event key:",
        key
    )

    print(
        "Number of records:",
        len(records)
    )

    for record in records:

        print()

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


# ==========================================================
# FINAL MESSAGE
# ==========================================================

print()
print("=" * 80)

print(
    "REAL DATA FUSION TEST COMPLETE"
)

print("=" * 80)