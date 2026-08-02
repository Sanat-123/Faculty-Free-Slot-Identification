from engine.entity_matcher import EntityMatcher
from database.knowledge_loader import KnowledgeLoader

print("=" * 60)
print("SUBJECT")
print("=" * 60)

result = EntityMatcher.match(
    "pyhton",
    KnowledgeLoader.get_subjects()
)

print(result)


print("\n" + "=" * 60)
print("TEACHER")
print("=" * 60)

result = EntityMatcher.match(
    "ashis pant",
    KnowledgeLoader.get_teachers()
)

print(result)


print("\n" + "=" * 60)
print("ROOM")
print("=" * 60)

result = EntityMatcher.match(
    "103",
    KnowledgeLoader.get_rooms()
)

print(result)


print("\n" + "=" * 60)
print("CLASS")
print("=" * 60)

result = EntityMatcher.match(
    "3cs ds a",
    KnowledgeLoader.get_classes()
)

print(result)