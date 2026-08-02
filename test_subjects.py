from database.knowledge_loader import KnowledgeLoader

knowledge = KnowledgeLoader.load()

print("=" * 80)
print("TOTAL SUBJECTS:", len(knowledge["subjects"]))
print("=" * 80)

for subject in sorted(knowledge["subjects"]):
    print(subject)