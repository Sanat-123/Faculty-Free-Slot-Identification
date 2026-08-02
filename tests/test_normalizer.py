import sys
import os

# Add the project root to Python's path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from engine.normalizer import Normalizer

queries = [
    "3cs ds a",
    "group1",
    "CL15",
    "cl 15",
    " Mr   Ashish   Pant ",
    "python"
]

for q in queries:
    print("=" * 50)
    print("Input      :", q)
    print("Normalized :", Normalizer.normalize(q))