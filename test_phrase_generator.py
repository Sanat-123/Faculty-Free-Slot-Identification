from engine.phrase_generator import PhraseGenerator

tokens = [

    "python",
    "for",
    "ds",
    "lab"

]

phrases = PhraseGenerator.generate(tokens)

for p in phrases:

    print(p)