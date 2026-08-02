from engine.query_tokenizer import QueryTokenizer
from engine.stopword_filter import StopWordFilter

queries = [

    "Who teaches Python?",

    "Show timetable of 3CS-DS-A",

    "Where is CL-15?",

    "Available faculty on Monday Slot 3",

    "Who teaches Python in 3CS-DS-A"

]

for q in queries:

    print("=" * 60)

    tokens = QueryTokenizer.tokenize(q)

    print("Original :", tokens)

    filtered = StopWordFilter.filter(tokens)

    print("Filtered :", filtered)