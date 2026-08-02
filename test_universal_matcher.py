from database.knowledge_loader import KnowledgeLoader
from engine.universal_matcher import UniversalMatcher

knowledge = KnowledgeLoader.load()

queries = [

    "ashis pant",

    "python",

    "103",

    "3cs ds a",

    "group 1"

]

for q in queries:

    print("=" * 60)

    print("Query :", q)

    print(UniversalMatcher.find(q, knowledge))