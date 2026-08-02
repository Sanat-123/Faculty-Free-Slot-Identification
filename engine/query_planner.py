from database.teacher_repository import TeacherRepository
from database.subject_repository import SubjectRepository
from database.timetable_repository import TimetableRepository


class QueryPlanner:
    """
    Converts an Intent + Extracted Entities + Day/Slot
    into a repository call.

    This class DOES NOT execute SQL directly.

    It only decides:
        1. Which repository to use
        2. Which method to call
        3. Which arguments to pass
    """

    @staticmethod
    def plan(intent, entities, day_slot):

        teacher = (
            entities["teachers"][0]["value"]
            if entities["teachers"] else None
        )

        subject = (
            entities["subjects"][0]["value"]
            if entities["subjects"] else None
        )

        room = (
            entities["rooms"][0]["value"]
            if entities["rooms"] else None
        )

        class_name = (
            entities["classes"][0]["value"]
            if entities["classes"] else None
        )

        group = (
            entities["groups"][0]["value"]
            if entities["groups"] else None
        )

        day = day_slot["day"]
        slot = day_slot["slot"]

        # ---------------------------------------------------
        # FIND TEACHER
        # ---------------------------------------------------

        if intent == "FIND_TEACHER":

            filters = {
                "subject": subject,
                "class": class_name,
                "group": group,
                "day": day,
                "slot": slot
            }

            return TeacherRepository.find_teacher(filters)

        # ---------------------------------------------------
        # FIND SUBJECT
        # ---------------------------------------------------

        if intent == "FIND_SUBJECT":

            filters = {
                "teacher": teacher,
                "class": class_name,
                "group": group,
                "day": day,
                "slot": slot
            }

            # Your current SubjectRepository does not yet
            # have find_subject(filters)

            if hasattr(SubjectRepository, "find_subject"):
                return SubjectRepository.find_subject(filters)

            return TimetableRepository.find_teacher(teacher)

        # ---------------------------------------------------
        # SHOW TIMETABLE
        # ---------------------------------------------------

        if intent == "SHOW_TIMETABLE":

            filters = {
                "teacher": teacher,
                "subject": subject,
                "class": class_name,
                "group": group,
                "room": room,
                "day": day,
                "slot": slot
            }

            return TimetableRepository.find(filters)

        # ---------------------------------------------------
        # FIND ROOM
        # ---------------------------------------------------

        if intent == "FIND_ROOM":

            filters = {
                "teacher": teacher,
                "subject": subject,
                "class": class_name,
                "group": group,
                "room": room,
                "day": day,
                "slot": slot
            }

            return TimetableRepository.find(filters)

        # ---------------------------------------------------
        # FIND FREE FACULTY
        # ---------------------------------------------------

        if intent == "FIND_FREE_FACULTY":

            filters = {
                "teacher": None,
                "subject": None,
                "class": None,
                "group": None,
                "room": None,
                "day": day,
                "slot": slot
            }

            busy_rows = TimetableRepository.find(filters)

            busy_teachers = {
                row[0]
                for row in busy_rows
            }

            all_teachers = TeacherRepository.get_all_teachers()

            free_teachers = sorted(
                set(all_teachers) - busy_teachers
            )

            return free_teachers

        # ---------------------------------------------------
        # UNKNOWN
        # ---------------------------------------------------

        return []