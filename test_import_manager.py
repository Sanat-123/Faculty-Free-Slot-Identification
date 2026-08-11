from import_engine.import_manager import ImportManager


print("=" * 80)
print("UNISCHED AI - UNIVERSAL IMPORT MANAGER TEST")
print("=" * 80)


# ==========================================================
# CREATE IMPORT MANAGER
# ==========================================================

manager = ImportManager()


# ==========================================================
# TEST FILE
# ==========================================================

FILE = r"data\timetable.xlsx"


# ==========================================================
# 1. DETECT FILE TYPE
# ==========================================================

print("\n1. FILE TYPE")
print("-" * 80)

file_type = manager.detect_file_type(FILE)

print("Detected type:", file_type)


# ==========================================================
# 2. VALIDATE FILE
# ==========================================================

print("\n2. FILE VALIDATION")
print("-" * 80)

validation = manager.validate_file(FILE)

for key, value in validation.items():
    print(f"{key}: {value}")


# ==========================================================
# 3. IMPORT FILE
# ==========================================================

print("\n3. IMPORT")
print("-" * 80)

result = manager.import_file(FILE)

print("Filename:", result.filename)
print("File type:", result.file_type)
print("Status:", result.status)
print("Dataset type:", result.dataset_type)
print("Record count:", result.record_count)


# ==========================================================
# 4. ERROR
# ==========================================================

if result.error:

    print("\nERROR")
    print("-" * 80)

    print(result.error)


# ==========================================================
# 5. DETECTED COLUMNS
# ==========================================================

print("\n4. DETECTED COLUMNS")
print("-" * 80)

for key, value in result.detected_columns.items():

    print(
        f"{key} -> {value}"
    )


# ==========================================================
# 6. WARNINGS
# ==========================================================

print("\n5. WARNINGS")
print("-" * 80)

if result.warnings:

    for warning in result.warnings:

        print(
            "WARNING:",
            warning
        )

else:

    print("No warnings.")


# ==========================================================
# 7. FIRST FIVE RECORDS
# ==========================================================

print("\n6. FIRST 5 RECORDS")
print("-" * 80)

for index, record in enumerate(
    result.records[:5],
    start=1
):

    print(
        f"\nRECORD {index}"
    )

    print("-" * 40)

    for key, value in record.items():

        print(
            f"{key}: {value}"
        )


# ==========================================================
# 8. FINAL STATUS
# ==========================================================

print("\n" + "=" * 80)

if result.status == "SUCCESS":

    print(
        "IMPORT MANAGER TEST PASSED"
    )

    print(
        f"Successfully imported "
        f"{result.record_count} records."
    )

else:

    print(
        "IMPORT MANAGER TEST FAILED"
    )

    print(
        "Error:",
        result.error
    )

print("=" * 80)