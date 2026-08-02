class StopWordFilter:
    """
    Removes common English words that
    do not represent timetable entities.

    This class is completely generic and
    works for any university.
    """

    STOP_WORDS = {

        "who",
        "what",
        "where",
        "when",
        "which",
        "why",
        "how",

        "is",
        "are",
        "was",
        "were",
        "be",
        "been",

        "the",
        "a",
        "an",

        "of",
        "in",
        "on",
        "at",
        "to",
        "for",
        "by",
        "with",
        "from",

        "show",
        "display",
        "find",
        "get",
        "give",
        "tell",

        "timetable",
        "schedule",

        "please"
    }

    @classmethod
    def filter(cls, tokens):

        return [

            token

            for token in tokens

            if token not in cls.STOP_WORDS

        ]