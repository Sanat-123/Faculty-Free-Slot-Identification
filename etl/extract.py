import pandas as pd
from pathlib import Path

# Project Root
BASE_DIR = Path(__file__).resolve().parent.parent

# Raw Data Folder
RAW = BASE_DIR / "data" / "raw"

# Processed Data Folder
PROCESSED = BASE_DIR / "data" / "processed"

# Create processed folder if it doesn't exist
PROCESSED.mkdir(parents=True, exist_ok=True)


def extract_csv(file_name):
    """
    Reads a CSV file from the raw folder.
    """

    file_path = RAW / file_name

    df = pd.read_csv(file_path)

    print(f"Loaded {file_name}")
    print(f"Rows    : {len(df)}")
    print(f"Columns : {len(df.columns)}")

    return df


def main():

    departments = extract_csv("departments.csv")
    courses = extract_csv("courses.csv")
    students = extract_csv("students.csv")
    faculty = extract_csv("faculty.csv")
    subjects = extract_csv("subjects.csv")
    attendance = extract_csv("attendance.csv")
    results = extract_csv("results.csv")
    fees = extract_csv("fees.csv")
    library_books = extract_csv("library_books.csv")
    library_transactions = extract_csv("library_transactions.csv")
    placements = extract_csv("placements.csv")
    hostel = extract_csv("hostel.csv")
    timetable = extract_csv("timetable.csv")
    exam_schedule = extract_csv("exam_schedule.csv")


if __name__ == "__main__":
    main()