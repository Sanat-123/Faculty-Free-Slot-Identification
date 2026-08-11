from pathlib import Path

from import_engine.import_manager import ImportManager
from dataset_manager.universal_dataset import UniversalDataset


print("=" * 80)
print("UNISCHED AI - ALL REAL DATASET FILES TEST")
print("=" * 80)


# ==========================================================
# ALL USER DATASET FILES
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
# PROCESS FILES
# ==========================================================

for file_path in FILES:

    print()
    print("=" * 80)

    print(
        "PROCESSING:",
        file_path.name
    )

    print("=" * 80)

    if not file_path.exists():

        print(
            "STATUS: FILE NOT FOUND"
        )

        print(
            "PATH:",
            file_path
        )

        continue

    result = manager.import_file(
        file_path
    )

    if result["success"]:

        print(
            "STATUS: SUCCESS"
        )

        print(
            "FILE TYPE:",
            result["file_type"]
        )

        print(
            "RECORDS:",
            result["record_count"]
        )

        dataset.add_records(
            result["records"]
        )

        # --------------------------------------------------
        # Inspection information
        # --------------------------------------------------

        inspection = result.get(
            "inspection"
        )

        if inspection:

            print()

            print(
                "DATASET TYPE:",
                inspection.get(
                    "dataset_type"
                )
            )

            print(
                "HAS DAY:",
                inspection.get(
                    "has_day"
                )
            )

            print(
                "HAS SLOT:",
                inspection.get(
                    "has_slot"
                )
            )

            print(
                "HAS TEACHER:",
                inspection.get(
                    "has_teacher"
                )
            )

        # --------------------------------------------------
        # Warnings
        # --------------------------------------------------

        warnings = result.get(
            "warnings",
            []
        )

        if warnings:

            print()

            print(
                "WARNINGS:"
            )

            for warning in warnings:

                print(
                    "  -",
                    warning
                )

    else:

        print(
            "STATUS: FAILED"
        )

        print(
            "ERROR:",
            result.get(
                "error"
            )
        )


# ==========================================================
# FINAL SUMMARY
# ==========================================================

print()
print("=" * 80)

print(
    "FINAL UNIVERSAL DATASET"
)

print("=" * 80)


summary = dataset.summary()


print(
    "Total records:",
    summary[
        "record_count"
    ]
)

print(
    "Total source files:",
    summary[
        "source_file_count"
    ]
)

print(
    "Teachers:",
    summary[
        "teacher_count"
    ]
)

print(
    "Subjects:",
    summary[
        "subject_count"
    ]
)

print(
    "Classes:",
    summary[
        "class_count"
    ]
)

print(
    "Rooms:",
    summary[
        "room_count"
    ]
)


print()
print(
    "SOURCE FILES:"
)

for source in summary[
    "source_files"
]:

    print(
        "  ✓",
        source
    )


print()
print("=" * 80)

print(
    "ALL REAL FILES TEST COMPLETE"
)

print("=" * 80)