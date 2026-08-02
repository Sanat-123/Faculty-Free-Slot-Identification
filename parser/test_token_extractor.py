from parser.components.token_extractor import TokenExtractor

while True:

    text = input("Input : ")

    tokens = TokenExtractor.extract(text)

    print()

    for i, token in enumerate(tokens):

        print(i, ":", token)

    print("-" * 40)