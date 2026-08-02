from chatbot.entity_extractor import EntityExtractor

while True:

    q = input("Ask : ")

    result = EntityExtractor.extract(q)

    print()

    for key, value in result.items():
        print(f"{key:10}: {value}")

    print("-" * 50)