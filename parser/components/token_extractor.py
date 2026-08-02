import re


class TokenExtractor:

    @staticmethod
    def extract(text: str):

        text = re.sub(r"\s+", " ", text).strip()

        tokens = text.split()

        return tokens