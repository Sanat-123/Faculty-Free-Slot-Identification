from database.db_manager import execute_query


class SubjectRepository:

    @staticmethod
    def get_all_subjects():

        rows = execute_query("""
            SELECT DISTINCT subject
            FROM timetable
            WHERE subject != ''
            ORDER BY subject
        """)

        return [row[0] for row in rows]