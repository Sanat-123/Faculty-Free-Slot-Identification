from import_engine.import_manager import ImportManager
from data_engine.canonical_event_matcher import CanonicalEventMatcher
from query_engine import QueryEngine


DATA_DIR = "data"

FILES = [
    "Facultywise TT 20 sep.pdf",
    "classwise TT 27 sep.pdf",
    "Location wise TT 27 sep 2025.pdf",
    "timetable.xlsx",
    "test_timetable.csv",
]


def main():

    print("=" * 80)
    print("UNISCHED AI - QUERY ENGINE TEST")
    print("=" * 80)

    # ---------------------------------------------------------
    # 1. IMPORT DATA
    # ---------------------------------------------------------

    manager = ImportManager()

    all_records = []

    for filename in FILES:

        path = f"{DATA_DIR}/{filename}"

        print(f"\nIMPORTING: {filename}")

        try:

            result = manager.import_file(path)

            if isinstance(result, dict):

                records = result.get(
                    "records",
                    []
                )

            else:

                records = result

            print(
                f"SUCCESS: {len(records)} records"
            )

            all_records.extend(records)

        except Exception as e:

            print(
                f"ERROR: {e}"
            )

    print("\n" + "=" * 80)
    print(
        f"TOTAL IMPORTED RECORDS: {len(all_records)}"
    )
    print("=" * 80)

    # ---------------------------------------------------------
    # 2. CANONICAL MATCHING
    # ---------------------------------------------------------

    matcher = CanonicalEventMatcher(
        all_records
    )

    matcher.match()

    summary = matcher.summary()

    print("\n" + "=" * 80)
    print("CANONICAL DATA")
    print("=" * 80)

    print(
        f"Canonical events : "
        f"{summary.get('canonical_events', len(matcher.events))}"
    )

    print(
        f"Faculty free     : "
        f"{summary.get('faculty_free_slots', len(matcher.faculty_free_slots))}"
    )

    print(
        f"Class free       : "
        f"{summary.get('class_free_slots', len(matcher.class_free_slots))}"
    )

    print(
        f"Room free        : "
        f"{summary.get('room_free_slots', len(matcher.room_free_slots))}"
    )

    print(
        f"Contracts        : "
        f"{summary.get('contract_records', len(matcher.contract_records))}"
    )

    # ---------------------------------------------------------
    # 3. CREATE QUERY ENGINE
    # ---------------------------------------------------------

    engine = QueryEngine(
        matcher
    )

    print("\n" + "=" * 80)
    print("QUERY ENGINE READY")
    print("=" * 80)

    # ---------------------------------------------------------
    # 4. DATASET SUMMARY
    # ---------------------------------------------------------

    print("\nDATASET SUMMARY")

    dataset_summary = engine.summary()

    for key, value in dataset_summary.items():

        print(
            f"{key}: {value}"
        )

    # ---------------------------------------------------------
    # 5. FACULTY FREE SLOT QUERY
    # ---------------------------------------------------------

    print("\n" + "=" * 80)
    print("QUERY 1 - FACULTY FREE SLOT")
    print("=" * 80)

    result = engine.faculty_free_slots(
        teacher="Dr. Mehul Mahrishi",
        day="Monday",
        slot=2
    )

    print(
        f"Count: {result['count']}"
    )

    for record in result["results"][:5]:

        print(record)

    # ---------------------------------------------------------
    # 6. TEACHER SCHEDULE
    # ---------------------------------------------------------

    print("\n" + "=" * 80)
    print("QUERY 2 - TEACHER SCHEDULE")
    print("=" * 80)

    result = engine.teacher_schedule(
        teacher="Dr. Mehul Mahrishi",
        day="Monday"
    )

    print(
        f"Scheduled events: {result['count']}"
    )

    for event in result["results"][:10]:

        print(
            f"Slot {event.get('slot')}: "
            f"{event.get('subject', '')} | "
            f"Room {event.get('room', '')} | "
            f"Class {event.get('class_name', '')}"
        )

    # ---------------------------------------------------------
    # 7. FACULTY STATUS
    # ---------------------------------------------------------

    print("\n" + "=" * 80)
    print("QUERY 3 - FACULTY STATUS")
    print("=" * 80)

    result = engine.faculty_status(
        teacher="Dr. Mehul Mahrishi",
        day="Monday",
        slot=3
    )

    print(
        f"Teacher : {result['teacher']}"
    )

    print(
        f"Day     : {result['day']}"
    )

    print(
        f"Slot    : {result['slot']}"
    )

    print(
        f"Status  : {result['status']}"
    )

    # ---------------------------------------------------------
    # 8. CLASS SCHEDULE
    # ---------------------------------------------------------

    print("\n" + "=" * 80)
    print("QUERY 4 - CLASS SCHEDULE")
    print("=" * 80)

    result = engine.class_schedule(
        class_name="3CS-D",
        day="Monday"
    )

    print(
        f"Events: {result['count']}"
    )

    for event in result["results"][:10]:

        print(
            f"Slot {event.get('slot')}: "
            f"{event.get('subject', '')} | "
            f"Teacher {event.get('teacher', '')}"
        )

    # ---------------------------------------------------------
    # 9. ROOM SCHEDULE
    # ---------------------------------------------------------

    print("\n" + "=" * 80)
    print("QUERY 5 - ROOM SCHEDULE")
    print("=" * 80)

    result = engine.room_schedule(
        room="303",
        day="Monday"
    )

    print(
        f"Events: {result['count']}"
    )

    for event in result["results"][:10]:

        print(
            f"Slot {event.get('slot')}: "
            f"{event.get('subject', '')} | "
            f"Teacher {event.get('teacher', '')}"
        )

    # ---------------------------------------------------------
    # 10. SUBJECT SEARCH
    # ---------------------------------------------------------

    print("\n" + "=" * 80)
    print("QUERY 6 - SUBJECT SEARCH")
    print("=" * 80)

    result = engine.subject_search(
        "OS III"
    )

    print(
        f"Results: {result['count']}"
    )

    for event in result["results"][:10]:

        print(
            f"{event.get('teacher', '')} | "
            f"{event.get('day', '')} | "
            f"Slot {event.get('slot', '')} | "
            f"Room {event.get('room', '')}"
        )

    # ---------------------------------------------------------
    # COMPLETE
    # ---------------------------------------------------------

    print("\n" + "=" * 80)
    print("QUERY ENGINE TEST COMPLETED")
    print("=" * 80)


if __name__ == "__main__":
    main()