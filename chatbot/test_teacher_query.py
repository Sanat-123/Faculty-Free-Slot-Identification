from chatbot.extractors.teacher_subject import TeacherSubjectExtractor
from database.teacher_repository import TeacherRepository

while True:

    question = input("Ask : ")

    entity = TeacherSubjectExtractor.extract(question)

    print("\nExtracted :", entity)

    teachers = TeacherRepository.find_by_subject(
        entity["subject"]
    )

    print("\nTeachers:")

    if teachers:
        for teacher in teachers:
            print("•", teacher)
    else:
        print("No teacher found.")

    print("-" * 60)