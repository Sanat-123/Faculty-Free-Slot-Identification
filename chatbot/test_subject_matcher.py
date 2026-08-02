from chatbot.subject_matcher import SubjectMatcher

while True:

    query = input("Ask : ")

    subject = SubjectMatcher.find_subject(query)

    print()

    print("Matched Subject :", subject)

    print("-" * 40)