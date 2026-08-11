from import_engine.pdf_importer import PDFImporter


print("=" * 80)
print("UNISCHED AI - PDF IMPORTER TEST")
print("=" * 80)


# ==========================================================
# CHANGE THIS TO ONE OF YOUR PDF FILES
# ==========================================================

FILE = r"data\Facultywise TT 20 sep.pdf"


# ==========================================================
# 1. VALIDATION
# ==========================================================

print("\n1. FILE VALIDATION")
print("-" * 80)

validation = PDFImporter.validate_file(FILE)

for key, value in validation.items():

    print(
        f"{key}: {value}"
    )


if not validation["valid"]:

    print(
        "\nPDF VALIDATION FAILED"
    )

    raise SystemExit


# ==========================================================
# 2. PDF INSPECTION
# ==========================================================

print("\n2. PDF INSPECTION")
print("-" * 80)

info = PDFImporter.inspect_file(
    FILE
)

for key, value in info.items():

    print(
        f"{key}: {value}"
    )


# ==========================================================
# 3. RAW TABLE EXTRACTION
# ==========================================================

print("\n3. RAW TABLE EXTRACTION")
print("-" * 80)

records = PDFImporter.import_file(
    FILE
)

print(
    "Extracted records:",
    len(records)
)


# ==========================================================
# 4. FIRST FIVE RECORDS
# ==========================================================

print("\n4. FIRST 5 RAW RECORDS")
print("-" * 80)

for index, record in enumerate(
    records[:5],
    start=1
):

    print(
        f"\nRECORD {index}"
    )

    print(
        "-" * 40
    )

    for key, value in record.items():

        print(
            f"{key}: {value}"
        )


# ==========================================================
# FINAL RESULT
# ==========================================================

print("\n" + "=" * 80)

if records:

    print(
        "PDF IMPORTER TEST PASSED"
    )

    print(
        f"Extracted {len(records)} raw table records."
    )

else:

    print(
        "PDF IMPORTER FOUND NO TABLE RECORDS."
    )

    print(
        "This does NOT necessarily mean the PDF is empty."
    )

    print(
        "It may use a layout that requires the next"
    )

    print(
        "PDF layout/OCR extraction layer."
    )

print("=" * 80)