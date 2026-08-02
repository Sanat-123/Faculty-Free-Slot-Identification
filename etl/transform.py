import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

RAW = BASE_DIR / "data" / "raw"
PROCESSED = BASE_DIR / "data" / "processed"

PROCESSED.mkdir(parents=True, exist_ok=True)


def clean_csv(file_name):

    print(f"\nProcessing {file_name}")

    df = pd.read_csv(RAW / file_name)

    print("Original Shape :", df.shape)

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Remove completely empty rows
    df = df.dropna(how="all")

    # Remove leading/trailing spaces
    df.columns = df.columns.str.strip()

    for col in df.select_dtypes(include="object"):
        df[col] = df[col].astype(str).str.strip()

    output_file = PROCESSED / file_name

    df.to_csv(output_file, index=False)

    print("Cleaned Shape :", df.shape)
    print(f"Saved -> {output_file.name}")


def main():

    files = [

        "departments.csv",
        "courses.csv",
        "students.csv",
        "faculty.csv",
        "subjects.csv",
        "attendance.csv",
        "results.csv",
        "fees.csv",
        "library_books.csv",
        "library_transactions.csv",
        "placements.csv",
        "hostel.csv",
        "timetable.csv",
        "exam_schedule.csv"

    ]

    for file in files:
        clean_csv(file)


if __name__ == "__main__":
    main()