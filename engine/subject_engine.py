from database.timetable_repository import TimetableRepository
from engine.table_printer import print_timetable


def find_subject(subject):

    return TimetableRepository.find_subject(subject)


if __name__ == "__main__":

    subject = input("Enter Subject : ").strip()

    rows = find_subject(subject)

    if rows:

        print(rows[0])
        print()

        print_timetable(
            rows,
            f"Subject Search : {subject}"
        )

    else:

        print("No records found.")