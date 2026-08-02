from engine.query_tokenizer import QueryTokenizer
from engine.stopword_filter import StopWordFilter
from engine.day_slot_extractor import DaySlotExtractor
from engine.entity_extractor import EntityExtractor
from engine.intent_detector import IntentDetector

extractor = EntityExtractor()

queries = [

    "Who teaches Python?",

    "Show timetable of 3CS-DS-A",

    "Where is Python for DS Lab?",

    "Available faculty on Monday Slot 3",

    "Show Group 1 timetable",

    "Subject of Dr Pankaj Dadheech"

]

for query in queries:

    print("=" * 80)

    print(query)

    # Step 1: Tokenize
    tokens = QueryTokenizer.tokenize(query)

    # Step 2: Remove stop words
    filtered_tokens = StopWordFilter.filter(tokens)

    # Step 3: Extract day & slot
    day_slot = DaySlotExtractor.extract(filtered_tokens)

    # Step 4: Extract entities ONLY from remaining tokens
    entities = extractor.extract(
        day_slot["remaining_tokens"]
    )

    # Step 5: Detect intent
    intent = IntentDetector.detect(
        tokens,
        entities,
        day_slot
    )

    print("Intent :", intent)
    print("Entities :", entities)
    print("Day/Slot :", day_slot)