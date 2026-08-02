from database.teacher_repository import TeacherRepository
from database.subject_repository import SubjectRepository
from database.db_manager import execute_query


class KnowledgeLoader:
    """
    Loads all dynamic data from the database.

    Nothing in this class is hardcoded.
    Whenever a new timetable PDF is uploaded and the
    database is rebuilt, these collections automatically
    reflect the latest data.
    """

    @staticmethod
    def get_teachers():
        return TeacherRepository.get_all_teachers()

    @staticmethod
    def get_subjects():
        return SubjectRepository.get_all_subjects()

    @staticmethod
    def get_rooms():

        rows = execute_query("""
            SELECT DISTINCT room
            FROM timetable
            WHERE room != ''
            ORDER BY room
        """)

        return [row[0] for row in rows if row[0]]

    @staticmethod
    def get_classes():

        rows = execute_query("""
            SELECT DISTINCT class_name
            FROM timetable
            WHERE class_name != ''
            ORDER BY class_name
        """)

        return [row[0] for row in rows if row[0]]

    @staticmethod
    def get_groups():

        rows = execute_query("""
            SELECT DISTINCT group_name
            FROM timetable
            WHERE group_name != ''
            ORDER BY group_name
        """)

        return [row[0] for row in rows if row[0]]

    @staticmethod
    def load():
        """
        Returns all knowledge in one dictionary.
        """

        return {
            "teachers": KnowledgeLoader.get_teachers(),
            "subjects": KnowledgeLoader.get_subjects(),
            "rooms": KnowledgeLoader.get_rooms(),
            "classes": KnowledgeLoader.get_classes(),
            "groups": KnowledgeLoader.get_groups()
        }