class ResponseGenerator:

    @staticmethod
    def generate(intent, result):

        if not result:
            return "No matching information found."

        # -----------------------------------------
        # FIND TEACHER
        # -----------------------------------------

        if intent == "FIND_TEACHER":

            teachers = sorted(set(result))

            return (
                "Teacher(s):\n\n"
                + "\n".join(
                    f"• {teacher}"
                    for teacher in teachers
                )
            )

        # -----------------------------------------
        # FIND FREE FACULTY
        # -----------------------------------------

        if intent == "FIND_FREE_FACULTY":

            return (
                f"Available Faculty ({len(result)}):\n\n"
                + "\n".join(
                    f"• {teacher}"
                    for teacher in result
                )
            )

        # -----------------------------------------
        # FIND SUBJECT
        # -----------------------------------------

        if intent == "FIND_SUBJECT":

            subjects = sorted({
                row[3]
                for row in result
            })

            return (
                "Subjects:\n\n"
                + "\n".join(
                    f"• {subject}"
                    for subject in subjects
                )
            )

        # -----------------------------------------
        # FIND ROOM
        # -----------------------------------------

        if intent == "FIND_ROOM":

            output = []

            for row in result:

                teacher, day, slot, subject, room, class_name, group, lecture_type = row

                output.append(

                    f"""
Subject : {subject}
Teacher : {teacher}
Day     : {day}
Slot    : {slot}
Room    : {room}
Class   : {class_name}
Group   : {group}
Type    : {lecture_type}
""".strip()

                )

            return "\n\n" + ("\n\n".join(output))

        # -----------------------------------------
        # SHOW TIMETABLE
        # -----------------------------------------

        if intent == "SHOW_TIMETABLE":

            output = []

            for row in result:

                teacher, day, slot, subject, room, class_name, group, lecture_type = row

                output.append(

                    f"""
Day     : {day}
Slot    : {slot}
Teacher : {teacher}
Subject : {subject}
Room    : {room}
Class   : {class_name}
Group   : {group}
Type    : {lecture_type}
""".strip()

                )

            return "\n\n".join(output)

        return str(result)