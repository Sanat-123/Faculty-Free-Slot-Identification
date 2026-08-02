from database.knowledge_loader import KnowledgeLoader
from engine.normalizer import Normalizer

knowledge = KnowledgeLoader.load()

query = "python"

print("Normalized Query:", Normalizer.normalize(query))
print()

for subject in knowledge["subjects"]:
    if "python" in subject.lower():
        print("Original :", subject)
        print("Normalized:", Normalizer.normalize(subject))
        print(
            "Startswith:",
            Normalizer.normalize(subject).startswith(
                Normalizer.normalize(query)
            )
        )