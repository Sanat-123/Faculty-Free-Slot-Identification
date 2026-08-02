from pprint import pprint

from engine.query_tokenizer import QueryTokenizer
from engine.stopword_filter import StopWordFilter
from engine.day_slot_extractor import DaySlotExtractor


queries = [

    "Available faculty on Monday Slot 3",

    "Who is free Tuesday Period 5",

    "Show timetable Wednesday",

    "Faculty available Friday 2",

    "Room available on Saturday Slot 7"

]

for query in queries:

    print("=" * 80)

    print(query)

    tokens = QueryTokenizer.tokenize(query)

    tokens = StopWordFilter.filter(tokens)

    pprint(
        DaySlotExtractor.extract(tokens)
    )