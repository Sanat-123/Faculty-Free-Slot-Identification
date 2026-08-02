"""
---------------------------------------------------------
Hostel Query Module
---------------------------------------------------------
"""

from db import execute_query


# ==========================================================
# TOTAL HOSTEL STUDENTS
# ==========================================================

def total_hostel_students():

    query = """
    SELECT COUNT(*)
    FROM warehouse.hostel;
    """

    result = execute_query(query)

    return f"🏠 Total Hostel Students : {result[0][0]}"


# ==========================================================
# LIST HOSTEL STUDENTS
# ==========================================================

def list_hostel_students(limit=10):

    query = f"""
    SELECT
        hostel_id,
        hostel_name,
        room_number,
        room_type,
        student_id
    FROM warehouse.hostel
    ORDER BY hostel_id
    LIMIT {limit};
    """

    result = execute_query(query)

    output = "\n🏠 Hostel Students\n"
    output += "-" * 80 + "\n"

    for row in result:

        output += (
            f"{row[0]} | "
            f"{row[1]} | "
            f"Room {row[2]} | "
            f"{row[3]} | "
            f"{row[4]}\n"
        )

    return output


# ==========================================================
# SEARCH STUDENT HOSTEL
# ==========================================================

def search_student_hostel(student_id):

    query = f"""
    SELECT
        hostel_name,
        room_number,
        room_type
    FROM warehouse.hostel
    WHERE student_id='{student_id}';
    """

    result = execute_query(query)

    if not result:
        return "Student is not allotted a hostel."

    row = result[0]

    return f"""
🏠 Hostel Details

Student ID : {student_id}
Hostel     : {row[0]}
Room No    : {row[1]}
Room Type  : {row[2]}
"""


# ==========================================================
# ROOM TYPE SUMMARY
# ==========================================================

def room_type_summary():

    query = """
    SELECT
        room_type,
        COUNT(*)
    FROM warehouse.hostel
    GROUP BY room_type
    ORDER BY COUNT(*) DESC;
    """

    result = execute_query(query)

    output = "\n🛏 Room Type Summary\n"
    output += "-" * 45 + "\n"

    for row in result:

        output += f"{row[0]} : {row[1]} Students\n"

    return output


# ==========================================================
# HOSTEL WISE STUDENT COUNT
# ==========================================================

def hostel_summary():

    query = """
    SELECT
        hostel_name,
        COUNT(*)
    FROM warehouse.hostel
    GROUP BY hostel_name
    ORDER BY hostel_name;
    """

    result = execute_query(query)

    output = "\n🏢 Hostel Summary\n"
    output += "-" * 45 + "\n"

    for row in result:

        output += f"{row[0]} : {row[1]} Students\n"

    return output


# ==========================================================
# TEST MODULE
# ==========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("HOSTEL QUERY MODULE")
    print("=" * 60)

    print("\nTotal Hostel Students")
    print(total_hostel_students())

    print("\nHostel Student List")
    print(list_hostel_students())

    print("\nSearch Student Hostel")
    print(search_student_hostel("S0001"))

    print("\nRoom Type Summary")
    print(room_type_summary())

    print("\nHostel Summary")
    print(hostel_summary())