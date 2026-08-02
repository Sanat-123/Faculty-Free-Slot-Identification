from database.knowledge_loader import KnowledgeLoader

print("=" * 60)
print("TEACHERS")
print("=" * 60)
print(KnowledgeLoader.get_teachers()[:5])

print("\n" + "=" * 60)
print("SUBJECTS")
print("=" * 60)
print(KnowledgeLoader.get_subjects()[:5])

print("\n" + "=" * 60)
print("ROOMS")
print("=" * 60)
print(KnowledgeLoader.get_rooms()[:10])

print("\n" + "=" * 60)
print("CLASSES")
print("=" * 60)
print(KnowledgeLoader.get_classes()[:10])

print("\n" + "=" * 60)
print("GROUPS")
print("=" * 60)
print(KnowledgeLoader.get_groups()[:10])