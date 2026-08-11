from pathlib import Path

from import_engine.import_manager import ImportManager
from dataset_manager.universal_dataset import UniversalDataset


print("=" * 80)
print("UNISCHED AI - MULTI FILE IMPORT TEST")
print("=" * 80)


# ==========================================================
# CREATE IMPORT MANAGER
# ==========================================================

manager = ImportManager()


# ==========================================================
# USER FILES
# ==========================================================

FILES = [

    Path(
        r"data\Facultywise TT 20 sep.pdf"
    ),

    Path(
        r"data\timetable.xlsx"
    ),

    Path(
        r"data\test_timetable.csv"
    ),

]


# ==========================================================
# UNIVERSAL DATASET
# ==========================================================

dataset = UniversalDataset()


# ==========================================================
# IMPORT FILES
# ==========================================================

for file_path in FILES:

    print()
    print("-" * 80)

    print(
        "Processing:",
        file_path.name
    )

    print("-" * 80)

    if not file_path.exists():

        print(
            "ERROR: File not found:"
        )

        print(
            file_path
        )

        continue

    result = manager.import_file(
        file_path
    )

    if result["success"]:

        print(
            "Status: SUCCESS"
        )

        print(
            "File type:",
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
            "Status: FAILED"
        )

        print(
            "Error:",
            result["error"]
        )


# ==========================================================
# FINAL DATASET
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
    summary["record_count"]
)

print(
    "Total source files:",
    summary["source_file_count"]
)

print(
    "Teachers:",
    summary["teacher_count"]
)

print(
    "Subjects:",
    summary["subject_count"]
)

print(
    "Classes:",
    summary["class_count"]
)

print(
    "Rooms:",
    summary["room_count"]
)


print()
print("SOURCE FILES")

for source in summary[
    "source_files"
]:

    print(
        "  ✓",
        source
    )


print()
print("=" * 80)

if summary["record_count"] > 0:

    print(
        "MULTI FILE IMPORT TEST PASSED"
    )

else:

    print(
        "MULTI FILE IMPORT TEST FAILED"
    )

print("=" * 80)