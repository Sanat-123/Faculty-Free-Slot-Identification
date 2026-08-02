from engine.query_tokenizer import QueryTokenizer
from engine.stopword_filter import StopWordFilter
from engine.day_slot_extractor import DaySlotExtractor
from engine.entity_extractor import EntityExtractor
from engine.intent_detector import IntentDetector
from engine.query_planner import QueryPlanner
from engine.response_generator import ResponseGenerator

extractor = EntityExtractor()

queries = [

    "Who teaches Python?",

    "Where is Python for DS Lab?",

    "Available faculty Monday Slot 3",

    "Show timetable of 3CS-DS-A",

    "Subject of Dr Pankaj Dadheech"

]

for query in queries:

    print("=" * 100)

    print(query)

    tokens = QueryTokenizer.tokenize(query)

    filtered = StopWordFilter.filter(tokens)

    day_slot = DaySlotExtractor.extract(filtered)

    entities = extractor.extract(
        day_slot["remaining_tokens"]
    )

    intent = IntentDetector.detect(
        tokens,
        entities,
        day_slot
    )

    result = QueryPlanner.plan(
        intent,
        entities,
        day_slot
    )

    response = ResponseGenerator.generate(
        intent,
        result
    )

    print()

    print(response)

    print()