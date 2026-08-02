from database.teacher_repository import TeacherRepository

teachers = TeacherRepository.get_all_teachers()

for teacher in teachers:
    print(teacher)