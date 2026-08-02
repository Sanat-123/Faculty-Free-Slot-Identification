from chatbot.teacher_matcher import TeacherMatcher

while True:

    query = input("Ask : ")

    teacher = TeacherMatcher.find_teacher(query)

    print()

    print("Matched Teacher :", teacher)

    print("-" * 40)