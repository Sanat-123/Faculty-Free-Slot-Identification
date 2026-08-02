from rapidfuzz import process, fuzz


class EntityMatcher:
    """
    Generic matcher for any type of entity.

    Works with:
        - Teachers
        - Subjects
        - Rooms
        - Classes
        - Groups

    No hardcoded values.
    """

    @staticmethod
    def match(query, entities, threshold=70):

        if not query:
            return None

        if not entities:
            return None

        match = process.extractOne(
            query,
            entities,
            scorer=fuzz.partial_ratio,
            score_cutoff=threshold
        )

        if not match:
            return None

        return {
            "value": match[0],
            "confidence": round(match[1], 2)
        }