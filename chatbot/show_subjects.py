from database.subject_repository import SubjectRepository

subjects = SubjectRepository.get_all_subjects()

for subject in subjects:
    print(subject)