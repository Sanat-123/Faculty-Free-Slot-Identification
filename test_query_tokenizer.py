from engine.query_tokenizer import QueryTokenizer

queries = [

    "Who teaches Python?",

    "Show timetable of 3CS-DS-A.",

    "Available faculty on Monday Slot 3",

    "Where is CL-15?",

    "Group-1 timetable"

]

for q in queries:

    print("="*60)

    print(q)

    print(QueryTokenizer.tokenize(q))