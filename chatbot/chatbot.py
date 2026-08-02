from chatbot.nlp_engine import analyze_query

from engine.free_slot_engine import find_free_faculty
from engine.subject_engine import find_subject
from database.timetable_repository import TimetableRepository
from engine.table_printer import print_timetable

print("=" * 70)
print("FACULTY FREE SLOT AI CHATBOT")
print("=" * 70)

while True:

    query = input("\nAsk me : ").strip()

    if query.lower() in ("exit", "quit"):
        print("\nGoodbye!")
        break

    # Analyze user query
    intent, day, slot, subject = analyze_query(query)

    print("\nDetected Information")
    print("-" * 40)
    print("Intent :", intent)
    print("Day    :", day)
    print("Slot   :", slot)
    print("Subject:", subject)

    # ==================================================
    # FREE FACULTY
    # ==================================================

    if intent == "FREE_FACULTY":

        if not day or not slot:
            print("\nPlease specify both day and slot.")
            continue

        teachers = find_free_faculty(day, slot)

        if teachers:

            print("\n" + "=" * 60)
            print(f"FREE FACULTY ON {day.upper()} SLOT {slot}")
            print("=" * 60)

            for i, teacher in enumerate(teachers, start=1):
                print(f"{i}. {teacher}")

            print("\nTotal Free Faculty :", len(teachers))

        else:

            print("\nNo free faculty found.")

    # ==================================================
    # SUBJECT SEARCH
    # ==================================================

    elif intent == "SUBJECT_SEARCH":

        if not subject:
            print("\nSubject not detected.")
            continue

        teachers = TimetableRepository.find_subject_teachers(subject)

        if teachers:

            print("\n" + "=" * 60)
            print(f"FACULTY TEACHING : {subject}")
            print("=" * 60)

            for i, teacher in enumerate(teachers, start=1):
                print(f"{i}. {teacher[0]}")

            print("\nTotal Faculty :", len(teachers))

        else:

            print("\nNo faculty found.")

    # ==================================================
    # UNKNOWN
    # ==================================================

    else:

        print("\nSorry, I couldn't understand your question.")
        print("\nExample Questions:")
        print("• Who teaches DSA?")
        print("• Who is free on Monday slot 3?")
        print("• Who teaches Python?")