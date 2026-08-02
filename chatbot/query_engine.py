"""
=========================================================
University Analytics Query Engine
=========================================================
"""

from student_queries import *
from faculty_queries import *
from department_queries import *
from placement_queries import *
from library_queries import *
from attendance_queries import *
from fee_queries import *
from hostel_queries import *


def chatbot_help():

    return """
================ UNIVERSITY ANALYTICS =================

Available Categories

1. Students
2. Faculty
3. Departments
4. Placements
5. Library
6. Attendance
7. Fees
8. Hostel

======================================================
"""


if __name__ == "__main__":

    print(chatbot_help())

    print("Students :", total_students())
    print("Faculty :", total_faculty())
    print("Departments :", total_departments())
    print("Companies :", total_companies())
    print("Books :", total_books())
    print(overall_attendance())
    print(total_fee_collection())
    print(total_hostel_students())