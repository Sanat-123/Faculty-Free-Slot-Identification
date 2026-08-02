import re

from database.teacher_repository import TeacherRepository


class TeacherMatcher:

    PREFIXES = [
        "dr.",
        "mr.",
        "mrs.",
        "ms.",
        "prof."
    ]

    @staticmethod
    def normalize(name):

        name = name.lower()

        for prefix in TeacherMatcher.PREFIXES:
            name = name.replace(prefix, "")

        name = re.sub(r"\s+", " ", name)

        return name.strip()

    @staticmethod
    def find_teacher(query):

        query = TeacherMatcher.normalize(query)

        teachers = TeacherRepository.get_all_teachers()

        for teacher in teachers:

            normalized_teacher = TeacherMatcher.normalize(teacher)

            if normalized_teacher in query:
                return teacher

        return ""