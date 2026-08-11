from import_engine.excel_importer import ExcelImporter


FILE = r"data\timetable.xlsx"


print("=" * 80)
print("UNISCHED AI - EXCEL IMPORTER TEST")
print("=" * 80)


# --------------------------------------------------
# Inspect Excel
# --------------------------------------------------

info = ExcelImporter.inspect_file(FILE)

print("\nDATASET INFORMATION")
print("-" * 80)

for key, value in info.items():
    print(f"{key}: {value}")


# --------------------------------------------------
# Import Excel
# --------------------------------------------------

records = ExcelImporter.import_file(FILE)

print("\n" + "=" * 80)
print("TOTAL IMPORTED RECORDS:", len(records))
print("=" * 80)


# --------------------------------------------------
# Display first 10 records
# --------------------------------------------------

for index, record in enumerate(records[:10], start=1):

    print(f"\nRECORD {index}")
    print("-" * 80)

    for key, value in record.items():
        print(f"{key}: {value}")