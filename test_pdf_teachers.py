import pdfplumber

from import_engine.pdf_importer import PDFImporter


FILE = r"data\Facultywise TT 20 sep.pdf"


print("=" * 80)
print("UNISCHED AI - PDF TEACHER DIAGNOSTIC")
print("=" * 80)


missing_pages = []


with pdfplumber.open(FILE) as pdf:

    print(f"\nTotal pages: {len(pdf.pages)}")

    for page_number, page in enumerate(
        pdf.pages,
        start=1
    ):

        teacher = PDFImporter.detect_teacher(
            page
        )

        if teacher:

            print(
                f"Page {page_number:3} : "
                f"{teacher}"
            )

        else:

            missing_pages.append(
                page_number
            )


print("\n" + "=" * 80)

print(
    "PAGES WHERE TEACHER WAS NOT DETECTED"
)

print("=" * 80)

print(
    missing_pages
)

print(
    f"\nMissing teacher pages: "
    f"{len(missing_pages)}"
)


# ----------------------------------------------------------
# Inspect words from missing pages
# ----------------------------------------------------------

if missing_pages:

    print("\n" + "=" * 80)

    print(
        "DETAILS OF FIRST MISSING PAGE"
    )

    print("=" * 80)

    page_number = missing_pages[0]

    with pdfplumber.open(FILE) as pdf:

        page = pdf.pages[
            page_number - 1
        ]

        words = page.extract_words(
            keep_blank_chars=False
        )

        print(
            f"\nPAGE: {page_number}"
        )

        print(
            f"WORD COUNT: {len(words)}"
        )

        print("\nWORDS:")

        for word in words:

            print(
                word
            )