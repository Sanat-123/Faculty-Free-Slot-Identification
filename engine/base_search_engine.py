from engine.table_printer import print_timetable
from database.faculty_repository import FacultyRepository


def run_search(prompt, title, search_function):

    search_text = input(prompt).strip()

    # Step 1 : Check whether teacher exists
    if title == "Teacher Timetable":

        if not FacultyRepository.teacher_exists(search_text):

            print("\n❌ Teacher not found.")
            print("Please enter a valid faculty name.\n")
            return

    # Step 2 : Search timetable
    rows = search_function(search_text)

    # Step 3 : Teacher exists but has no classes
    if not rows:

        print("\nℹ️ Teacher found.")
        print("No classes are assigned to this faculty member.\n")
        return

    # Step 4 : Display timetable
    print_timetable(
        rows,
        f"{title} : {search_text}"
    )