import re


class QueryTokenizer:
    """
    Universal tokenizer.

    Responsibilities:
    - lowercase
    - remove punctuation
    - preserve hyphenated words
    - split into tokens

    Completely independent of
    any university.
    """

    @staticmethod
    def tokenize(query):

        if not query:
            return []

        query = query.lower()

        query = re.sub(r"[^\w\s-]", " ", query)

        query = re.sub(r"\s+", " ", query).strip()

        return query.split()