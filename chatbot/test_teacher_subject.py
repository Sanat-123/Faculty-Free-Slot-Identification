from chatbot.extractors.teacher_subject import TeacherSubjectExtractor

while True:

    q = input("Ask : ")

    print()

    result = TeacherSubjectExtractor.extract(q)

    for k, v in result.items():
        print(f"{k:8}: {v}")

    print("-" * 60)