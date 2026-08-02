import sqlite3
import os
from utils.validator import is_valid_teacher

DB_FILE = os.path.join("database", "faculty.db")


def find_free_faculty(day, slot):

    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    # Get all teachers
    cursor.execute("""
        SELECT DISTINCT teacher
        FROM timetable
    """)

    all_teachers = {row[0] for row in cursor.fetchall()}

    # Get busy teachers
    cursor.execute("""
        SELECT DISTINCT teacher
        FROM timetable
        WHERE day = ?
        AND slot = ?
    """, (day, slot))

    busy_teachers = {row[0] for row in cursor.fetchall()}

    print("Busy Teachers:", len(busy_teachers))
    print(busy_teachers)

    connection.close()

    free_teachers = sorted(all_teachers - busy_teachers)

    print("Before Validation:", free_teachers[:10])

    free_teachers = [
        teacher
        for teacher in free_teachers
        if is_valid_teacher(teacher)
    ]

    print("After Validation:", free_teachers[:10])

    return free_teachers

# ----------------------------------------------------
# This code runs ONLY when this file is executed directly
# ----------------------------------------------------

if __name__ == "__main__":

    print("=" * 60)
    print("FACULTY FREE SLOT SEARCH")
    print("=" * 60)

    day = input("Enter Day: ").strip()

    slot = int(input("Enter Slot: "))

    teachers = find_free_faculty(day, slot)

    print("\nFree Faculty\n")

    for i, teacher in enumerate(teachers, start=1):
        print(f"{i}. {teacher}")

    print("\nTotal Free Faculty:", len(teachers))