import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine

BASE_DIR = Path(__file__).resolve().parent.parent

PROCESSED = BASE_DIR / "data" / "processed"

DB_USER = "postgres"
DB_PASSWORD = "postgres123"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "university_dw"

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

SCHEMA = "warehouse"


def load_table(file_name):

    path = PROCESSED / file_name

    df = pd.read_csv(path)

    table_name = file_name.replace(".csv", "")

    df.to_sql(
        table_name,
        engine,
        schema=SCHEMA,
        if_exists="append",
        index=False
    )

    print(f"Loaded {table_name} ({len(df)} rows)")


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
        load_table(file)


if __name__ == "__main__":
    main()