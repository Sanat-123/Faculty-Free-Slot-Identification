from import_engine.import_manager import ImportManager
from data_engine.canonical_event_matcher import CanonicalEventMatcher
from query_engine import (
    QueryEngine,
    NaturalLanguageQuery,
)


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
    print("UNISCHED AI - NATURAL LANGUAGE QUERY TEST")
    print("=" * 80)

    # ---------------------------------------------------------
    # IMPORT
    # ---------------------------------------------------------

    manager = ImportManager()

    records = []

    for filename in FILES:

        path = f"{DATA_DIR}/{filename}"

        print(f"\nIMPORTING: {filename}")

        try:

            result = manager.import_file(path)

            if isinstance(result, dict):

                imported = result.get(
                    "records",
                    []
                )

            else:

                imported = result

            print(
                f"SUCCESS: {len(imported)} records"
            )

            records.extend(imported)

        except Exception as e:

            print(
                f"ERROR: {e}"
            )

    print("\n" + "=" * 80)
    print(
        f"TOTAL RECORDS: {len(records)}"
    )
    print("=" * 80)

    # ---------------------------------------------------------
    # CANONICAL MATCHING
    # ---------------------------------------------------------

    matcher = CanonicalEventMatcher(
        records
    )

    matcher.match()

    print(
        f"\nCanonical events: "
        f"{len(matcher.events)}"
    )

    print(
        f"Faculty free slots: "
        f"{len(matcher.faculty_free_slots)}"
    )

    print(
        f"Class free slots: "
        f"{len(matcher.class_free_slots)}"
    )

    print(
        f"Room free slots: "
        f"{len(matcher.room_free_slots)}"
    )

    print(
        f"Contract records: "
        f"{len(matcher.contract_records)}"
    )

    # ---------------------------------------------------------
    # QUERY ENGINE
    # ---------------------------------------------------------

    engine = QueryEngine(
        matcher
    )

    nlp = NaturalLanguageQuery(
        engine
    )

    # ---------------------------------------------------------
    # TEST QUERIES
    # ---------------------------------------------------------

    queries = [

        "Which faculty is free on Monday slot 2?",

        "Is Dr. Mehul Mahrishi free on Monday slot 3?",

        "What is Dr. Mehul Mahrishi teaching on Monday?",

        "Who teaches OS III?",

        "What is the schedule of Dr. Mehul Mahrishi on Monday?",

        "What is the timetable of 3CS-D on Monday?",

        "Which room is free on Monday slot 4?",

    ]

    # ---------------------------------------------------------
    # RUN QUERIES
    # ---------------------------------------------------------

    for number, query in enumerate(
        queries,
        1
    ):

        print("\n" + "=" * 80)

        print(
            f"QUERY {number}"
        )

        print("=" * 80)

        print(
            f"Question: {query}"
        )

        print()

        result = nlp.execute(
            query
        )

        print(
            f"Intent: {result.get('intent')}"
        )

        print(
            f"Success: {result.get('success')}"
        )

        print(
            f"Count: {result.get('count')}"
        )

        print()

        print(
            nlp.answer(query)
        )

    # ---------------------------------------------------------
    # COMPLETE
    # ---------------------------------------------------------

    print("\n" + "=" * 80)
    print("NATURAL LANGUAGE QUERY TEST COMPLETED")
    print("=" * 80)


if __name__ == "__main__":

    main()