import json
import os

JSON_FILE = os.path.join("database", "faculty_database.json")


class FacultyRepository:

    @staticmethod
    def teacher_exists(name):

        with open(JSON_FILE, "r", encoding="utf-8") as file:
            database = json.load(file)

        name = name.lower().strip()

        for teacher in database.keys():

            if name in teacher.lower():
                return True

        return False