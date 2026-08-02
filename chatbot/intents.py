"""
=========================================================
University Analytics Intent Engine
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


def process_query(query):

    query = query.lower().strip()

    # =====================================================
    # STUDENTS
    # =====================================================

    if "total student" in query or "how many student" in query:
        return f"🎓 Total Students : {total_students()}"

    elif "list student" in query:
        return list_students()

    elif query.startswith("student "):
        sid = query.split()[-1].upper()
        return search_student(sid)

    # =====================================================
    # FACULTY
    # =====================================================

    elif "total faculty" in query:
        return f"👨‍🏫 Total Faculty : {total_faculty()}"

    elif "list faculty" in query:
        return list_faculty()

    elif query.startswith("faculty "):
        name = query.replace("faculty", "").strip()
        return search_faculty(name)

    # =====================================================
    # DEPARTMENT
    # =====================================================

    elif "department" in query and "list" in query:
        return list_departments()

    elif query.startswith("department "):
        dept = query.replace("department", "").strip()
        return search_department(dept)

    # =====================================================
    # PLACEMENTS
    # =====================================================

    elif "highest package" in query:
        return highest_package()

    elif "average package" in query:
        return average_package()

    elif "companies" in query:
        return list_companies()

    elif "top hiring" in query:
        return top_companies()

    # =====================================================
    # LIBRARY
    # =====================================================

    elif "books" in query:
        return list_books()

    elif query.startswith("book "):
        book = query.replace("book", "").strip()
        return search_book(book)

    elif query.startswith("author "):
        author = query.replace("author", "").strip()
        return search_author(author)

    # =====================================================
    # ATTENDANCE
    # =====================================================

    elif "overall attendance" in query:
        return overall_attendance()

    elif "top attendance" in query:
        return top_attendance()

    elif "low attendance" in query:
        return low_attendance()

    elif query.startswith("attendance "):
        sid = query.split()[-1].upper()
        return student_attendance(sid)

    # =====================================================
    # FEES
    # =====================================================

    elif "fee summary" in query:
        return fee_status_summary()

    elif "total fee" in query:
        return total_fee_collection()

    elif "pending fee" in query:
        return total_pending_fee()

    elif query.startswith("fee "):
        sid = query.split()[-1].upper()
        return student_fee(sid)

    # =====================================================
    # HOSTEL
    # =====================================================

    elif "hostel summary" in query:
        return hostel_summary()

    elif "room type" in query:
        return room_type_summary()

    elif "hostel students" in query:
        return list_hostel_students()

    elif query.startswith("hostel "):
        sid = query.split()[-1].upper()
        return search_student_hostel(sid)

    # =====================================================

    else:
        return """
❌ I didn't understand your question.

Try:

• total students
• total faculty
• list departments
• highest package
• companies
• books
• attendance S0001
• fee S0001
• hostel S0001
"""