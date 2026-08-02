from parser.components.phrase_extractor import PhraseExtractor

while True:

    text = input("Input : ")

    phrases = PhraseExtractor.extract(text)

    print()

    for i, phrase in enumerate(phrases):

        print(i, ":", phrase)

    print("-" * 40)