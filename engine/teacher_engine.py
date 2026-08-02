from database.timetable_repository import TimetableRepository
from engine.base_search_engine import run_search


if __name__ == "__main__":

    run_search(
        prompt="Enter Teacher Name : ",
        title="Teacher Timetable",
        search_function=TimetableRepository.find_teacher
    )