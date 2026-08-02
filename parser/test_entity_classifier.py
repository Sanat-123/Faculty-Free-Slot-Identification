from parser.components.token_extractor import TokenExtractor
from parser.components.entity_classifier import EntityClassifier

while True:

    text = input("Input : ")

    tokens = TokenExtractor.extract(text)

    result = EntityClassifier.classify(tokens)

    print()

    for key, value in result.items():
        print(f"{key:8} : {value}")

    print("-" * 40)