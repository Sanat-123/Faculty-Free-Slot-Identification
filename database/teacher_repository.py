from database.db_manager import execute_query


class TeacherRepository:

    @staticmethod
    def get_all_teachers():

        rows = execute_query("""
            SELECT DISTINCT teacher
            FROM timetable
            ORDER BY teacher
        """)

        return [row[0] for row in rows if row[0]]

    @staticmethod
    def find_teacher(filters):

        sql = """
        SELECT DISTINCT teacher
        FROM timetable
        WHERE 1=1
        """

        parameters = []

        if filters["subject"]:
            sql += " AND subject = ?"
            parameters.append(filters["subject"])

        if filters["class"]:
            sql += " AND class_name = ?"
            parameters.append(filters["class"])

        if filters["group"]:
            sql += " AND group_name = ?"
            parameters.append(filters["group"])

        if filters["day"]:
            sql += " AND day = ?"
            parameters.append(filters["day"])

        if filters["slot"]:
            sql += " AND slot = ?"
            parameters.append(filters["slot"])

        sql += " ORDER BY teacher"

        rows = execute_query(sql, tuple(parameters))

        return [row[0] for row in rows if row[0]]