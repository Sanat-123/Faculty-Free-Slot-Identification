from database.db_manager import execute_query
from engine.table_printer import print_timetable



def find_class(class_name):

    query = """
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
        WHERE class_name LIKE ?
        ORDER BY day, slot
    """

    return execute_query(
        query,
        ("%" + class_name + "%",)
    )

if __name__ == "__main__":

   class_name = input("Enter Class Name : ").strip()

rows = find_class(class_name)

print_timetable(
    rows,
    f"Class Timetable : {class_name}"
)

