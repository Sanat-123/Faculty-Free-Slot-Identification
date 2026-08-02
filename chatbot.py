from engine.query_tokenizer import QueryTokenizer
from engine.stopword_filter import StopWordFilter
from engine.day_slot_extractor import DaySlotExtractor
from engine.entity_extractor import EntityExtractor
from engine.intent_detector import IntentDetector
from engine.query_planner import QueryPlanner
from engine.response_generator import ResponseGenerator


class FacultyAIChatbot:

    def __init__(self):

        print("\nLoading Knowledge Base...")

        self.extractor = EntityExtractor()

        print("Knowledge Base Loaded Successfully!")

    def process_query(self, query):

        # -------------------------
        # Step 1 : Tokenization
        # -------------------------

        tokens = QueryTokenizer.tokenize(query)

        # -------------------------
        # Step 2 : Stopword Removal
        # -------------------------

        filtered_tokens = StopWordFilter.filter(tokens)

        # -------------------------
        # Step 3 : Day & Slot Extraction
        # -------------------------

        day_slot = DaySlotExtractor.extract(filtered_tokens)

        # -------------------------
        # Step 4 : Entity Extraction
        # -------------------------

        entities = self.extractor.extract(
            day_slot["remaining_tokens"]
        )

        # -------------------------
        # Step 5 : Intent Detection
        # -------------------------

        intent = IntentDetector.detect(
            tokens,
            entities,
            day_slot
        )

        # -------------------------
        # Step 6 : Query Planning
        # -------------------------

        result = QueryPlanner.plan(
            intent,
            entities,
            day_slot
        )

        # -------------------------
        # Step 7 : Response Generation
        # -------------------------

        response = ResponseGenerator.generate(
            intent,
            result
        )

        return response


def main():

    print("=" * 70)
    print("        FACULTY FREE SLOT AI ASSISTANT")
    print("=" * 70)

    print("\nExamples:")
    print("• Who teaches Python?")
    print("• Show timetable of 3CS-DS-A")
    print("• Where is Python for DS Lab?")
    print("• Available faculty Monday Slot 3")
    print("• Subject of Dr Pankaj Dadheech")
    print("\nType 'exit' to quit.\n")

    chatbot = FacultyAIChatbot()

    while True:

        try:

            query = input("\nYou : ").strip()

            if not query:
                continue

            if query.lower() in {
                "exit",
                "quit",
                "bye"
            }:
                print("\nAssistant : Goodbye! Have a nice day.")
                break

            response = chatbot.process_query(query)

            print("\nAssistant:\n")
            print(response)

        except KeyboardInterrupt:

            print("\n\nAssistant : Session terminated.")
            break

        except Exception as e:

            print("\nAssistant : Something went wrong.")
            print(e)


if __name__ == "__main__":
    main()