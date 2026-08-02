from database.db_manager import execute_query
from engine.table_printer import print_timetable
from utils.sql_constants import DAY_ORDER


def find_location(location):
    query = f"""
SELECT
    teacher,
    day,
    slot,
    subject,
    room,
    class_name,
    group_name,
    type
FROM timetable
WHERE room LIKE ?
ORDER BY
    {DAY_ORDER},
    slot
"""
    return execute_query(
        query,
        ("%" + location + "%",)
    )

if __name__ == "__main__":
    location = input("Enter Location : ").strip()

    rows = find_location(location)

    print_timetable(
        rows,
        f"Location Search : {location}"
    )

