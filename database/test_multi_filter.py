from database.timetable_repository import TimetableRepository

while True:

    filters = {

        "teacher": "",

        "subject": input("Subject : "),

        "class": input("Class : "),

        "group": input("Group : "),

        "room": input("Room : "),

        "day": input("Day : "),

        "slot": input("Slot : ")
    }

    if filters["slot"]:
        filters["slot"] = int(filters["slot"])

    rows = TimetableRepository.find(filters)

    print()

    print("Rows :", len(rows))

    print()

    for row in rows:
        print(row)

    print("=" * 80)