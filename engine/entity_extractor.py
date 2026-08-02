from database.knowledge_loader import KnowledgeLoader
from engine.phrase_generator import PhraseGenerator
from engine.universal_matcher import UniversalMatcher


class EntityExtractor:

    def __init__(self):

        self.knowledge = KnowledgeLoader.load()

    def extract(self, tokens):

        phrases = PhraseGenerator.generate(tokens)

        consumed = set()

        entities = {
            "teachers": [],
            "subjects": [],
            "rooms": [],
            "classes": [],
            "groups": []
        }

        # Longest phrases first
        phrases.sort(
            key=lambda p: (
                -(p["end"] - p["start"]),
                p["start"]
            )
        )

        for phrase in phrases:

            if any(
                idx in consumed
                for idx in range(
                    phrase["start"],
                    phrase["end"]
                )
            ):
                continue

            best = None

            for entity_type in entities.keys():

                result = UniversalMatcher.find_by_type(
                    phrase["text"],
                    self.knowledge[entity_type]
                )

                if result is None:
                    continue

                if (
                    best is None
                    or
                    result["confidence"] > best["confidence"]
                ):

                    best = {
                        "type": entity_type,
                        "value": result["value"],
                        "confidence": result["confidence"]
                    }

            if best is None:
                continue

            entities[best["type"]].append({
                "value": best["value"],
                "confidence": best["confidence"]
            })

            for idx in range(
                phrase["start"],
                phrase["end"]
            ):
                consumed.add(idx)

        return entities