from pprint import pprint

from engine.entity_extractor import EntityExtractor

extractor = EntityExtractor()

queries = [

    "Who teaches Python?",

    "Where is CL-15?",

    "Show timetable of 3CS-DS-A",

    "Show Group 1 timetable",

    "Who teaches Python in 3CS-DS-A",

    "Where is Python for DS Lab?",

    "Available faculty on Monday Slot 3",

    "Show timetable of Group 1 of 3CS-DS-A"

]

for query in queries:

    print("=" * 80)

    print(query)

    pprint(extractor.extract(query))