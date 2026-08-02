from database.knowledge_loader import KnowledgeLoader

knowledge = KnowledgeLoader.load()

print()

for key, value in knowledge.items():

    print(f"{key} : {len(value)}")