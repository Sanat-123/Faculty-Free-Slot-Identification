from rapidfuzz import process, fuzz


class SpellCorrector:
    """
    Generic Spell Corrector.

    This class does not know anything about teachers,
    subjects, rooms, classes, or groups.

    It simply finds the closest match from the list
    of entities provided.
    """

    @staticmethod
    def correct(word, entities, threshold=60):

        if not word or not entities:
            return word

        match = process.extractOne(
            word,
            entities,
            scorer=fuzz.partial_ratio,
            score_cutoff=threshold
        )

        if match:
            return match[0]

        return word