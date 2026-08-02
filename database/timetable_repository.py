from database.db_manager import execute_query
from utils.sql_constants import DAY_ORDER
from utils.search_modes import EXACT, PARTIAL, PREFIX


class TimetableRepository:

    ALLOWED_COLUMNS = frozenset({
        "teacher",
        "subject",
        "class_name",
        "room"
    })

    @staticmethod
    def _search(column, value, mode=PARTIAL):

        if column not in TimetableRepository.ALLOWED_COLUMNS:
            raise ValueError(f"Invalid column: {column}")

        value = " ".join(value.split()).strip()

        if mode == EXACT:
            operator = "="
            parameter = value

        elif mode == PREFIX:
            operator = "LIKE"
            parameter = f"{value}%"

        elif mode == PARTIAL:
            operator = "LIKE"
            parameter = f"%{value}%"

        else:
            raise ValueError(f"Invalid search mode: {mode}")

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
WHERE LOWER({column}) {operator} LOWER(?)
ORDER BY
    {DAY_ORDER},
    slot
"""

        return execute_query(
            query,
            (parameter,)
        )

    @staticmethod
    def find_teacher(name, mode=PARTIAL):

        return TimetableRepository._search(
            "teacher",
            name,
            mode
        )

    @staticmethod
    def find_subject(subject, mode=PARTIAL):

        return TimetableRepository._search(
            "subject",
            subject,
            mode
        )

    @staticmethod
    def find_subject_teachers(subject):

        query = """
SELECT DISTINCT teacher
FROM timetable
WHERE LOWER(subject) LIKE LOWER(?)
ORDER BY teacher
"""

        return execute_query(
            query,
            ("%" + subject + "%",)
        )

    @staticmethod
    def find_class(class_name, mode=PARTIAL):

        return TimetableRepository._search(
            "class_name",
            class_name,
            mode
        )

    @staticmethod
    def find_location(location, mode=EXACT):

        return TimetableRepository._search(
            "room",
            location,
            mode
        )

    @staticmethod
    def find(filters):

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
WHERE 1=1
"""

        parameters = []

        if filters["teacher"]:
            query += " AND teacher = ?"
            parameters.append(filters["teacher"])

        if filters["subject"]:
            query += " AND subject = ?"
            parameters.append(filters["subject"])

        if filters["class"]:
            query += " AND class_name = ?"
            parameters.append(filters["class"])

        if filters["group"]:
            query += " AND group_name = ?"
            parameters.append(filters["group"])

        if filters["room"]:
            query += " AND room = ?"
            parameters.append(filters["room"])

        if filters["day"]:
            query += " AND day = ?"
            parameters.append(filters["day"])

        if filters["slot"]:
            query += " AND slot = ?"
            parameters.append(filters["slot"])

        query += f"""
ORDER BY
    {DAY_ORDER},
    slot
"""

        return execute_query(
            query,
            tuple(parameters)
        )


# --------------------------------------------------
# TEST CODE (Runs only when this file is executed)
# --------------------------------------------------

if __name__ == "__main__":

    rows = execute_query("""
        SELECT DISTINCT subject
        FROM timetable
        ORDER BY subject
    """)

    for row in rows:
        print(row[0])