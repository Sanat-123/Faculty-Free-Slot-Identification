from chatbot.spell_corrector import SpellCorrector

print("=" * 50)
print("SUBJECT TESTS")
print("=" * 50)

tests = [
    "pyhton",
    "dbmss",
    "oprating system",
    "machin learning",
    "python lab"
]

for word in tests:
    print(f"{word} --> {SpellCorrector.correct_subject(word)}")


print("\n" + "=" * 50)
print("TEACHER TESTS")
print("=" * 50)

tests = [
    "ashis pant",
    "manish bhardwaj",
    "archika jain"
]

for word in tests:
    print(f"{word} --> {SpellCorrector.correct_teacher(word)}")