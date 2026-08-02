class PhraseGenerator:

    @staticmethod
    def generate(tokens, max_length=4):
        """
        Generate phrases from longest to shortest.

        Example:
        Tokens:
            python for ds lab

        Output:
            python for ds lab
            python for ds
            for ds lab
            python for
            for ds
            ds lab
            python
            for
            ds
            lab
        """

        phrases = []

        n = len(tokens)

        for length in range(min(max_length, n), 0, -1):

            for start in range(n - length + 1):

                phrase = " ".join(tokens[start:start + length])

                phrases.append(
                    {
                        "text": phrase,
                        "tokens": tokens[start:start + length],
                        "start": start,
                        "end": start + length
                    }
                )

        return phrases