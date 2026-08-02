from rapidfuzz import process, fuzz

from engine.normalizer import Normalizer


class UniversalMatcher:
    """
    Universal Matcher V2

    Matching Strategy
    -----------------
    1. Normalize query
    2. Exact match
    3. Normalized exact match
    4. High-quality fuzzy match

    No spell correction is performed here.
    Spell correction belongs in the NLP pipeline.
    """

    @staticmethod
    def find(query, knowledge, threshold=85):

        best = None

        for entity_type, entities in knowledge.items():

            result = UniversalMatcher.find_by_type(
                query,
                entities,
                threshold
            )

            if result is None:
                continue

            if best is None or result["confidence"] > best["confidence"]:

                best = {
                    "type": entity_type,
                    "value": result["value"],
                    "confidence": result["confidence"]
                }

        return best

    @staticmethod
    def find_by_type(query, entities, threshold=88):
        if not query or not entities:
            return None

        query = Normalizer.normalize_for_match(query)

        # -----------------------------
        # Build normalized lookup
        # -----------------------------
        normalized_entities = {
            Normalizer.normalize_for_match(entity): entity
            for entity in entities
        }

        # -----------------------------
        # STEP 1 : Exact Match
        # -----------------------------
        if query in normalized_entities:
            return {
                "value": normalized_entities[query],
                "confidence": 100.0
            }

        # -----------------------------
        # STEP 2 : Prefix Match
        # -----------------------------
        prefix_matches = []

        for normalized, original in normalized_entities.items():
            if normalized.startswith(query):
                prefix_matches.append(original)

        if len(prefix_matches) == 1:
            return {
                "value": prefix_matches[0],
                "confidence": 98.0
            }
        elif len(prefix_matches) > 1:
            # Prefer the shortest matching entity
            best = min(prefix_matches, key=len)
            return {
                "value": best,
                "confidence": 97.0
            }

        # -----------------------------
        # STEP 3 : High Quality Fuzzy Match
        # -----------------------------
        fuzzy = process.extractOne(
            query,
            normalized_entities.keys(),
            scorer=fuzz.WRatio,
            score_cutoff=threshold
        )

        if fuzzy:
            normalized_value = fuzzy[0]
            return {
                "value": normalized_entities[normalized_value],
                "confidence": round(fuzzy[1], 2)
            }

        return None

    @staticmethod
    def find_all(tokens, knowledge, threshold=85):

        results = {}

        for token in tokens:

            entity = UniversalMatcher.find(
                token,
                knowledge,
                threshold
            )

            if entity is None:
                continue

            entity_type = entity["type"]

            if entity_type not in results:
                results[entity_type] = []

            results[entity_type].append(entity)

        return results