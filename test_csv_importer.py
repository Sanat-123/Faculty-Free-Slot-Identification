from import_engine.import_manager import ImportManager


print("=" * 80)
print("UNISCHED AI - CSV IMPORTER TEST")
print("=" * 80)

manager = ImportManager()

# Change this to your actual CSV file when testing.
FILE = r"data\test_timetable.csv"

print("\n1. FILE TYPE")
print("-" * 80)

print(
    "Detected type:",
    manager.detect_file_type(FILE)
)

print("\n2. FILE VALIDATION")
print("-" * 80)

validation = manager.validate_file(FILE)

for key, value in validation.items():
    print(f"{key}: {value}")

print("\n3. IMPORT")
print("-" * 80)

result = manager.import_file(FILE)

manager.print_result(result)

if result.status == "SUCCESS":

    print("\nCSV IMPORT TEST PASSED")
    print(
        f"Successfully imported "
        f"{result.record_count} records."
    )

else:

    print("\nCSV IMPORT TEST FAILED")
    print("Error:", result.error)