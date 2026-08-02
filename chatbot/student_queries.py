"""
---------------------------------------------------------
Student Query Module
---------------------------------------------------------
"""

from db import execute_query


# ==========================================================
# TOTAL STUDENTS
# ==========================================================

def total_students():

    query = """
    SELECT COUNT(*)
    FROM warehouse.students;
    """

    return execute_query(query)[0][0]


# ==========================================================
# LIST STUDENTS
# ==========================================================

def list_students(limit=10):

    query = f"""
    SELECT student_id,
           first_name,
           last_name,
           gender,
           email
    FROM warehouse.students
    ORDER BY student_id
    LIMIT {limit};
    """

    result = execute_query(query)

    if not result:
        return "No students found."

    output = "\n📋 Student List\n"
    output += "-" * 70 + "\n"

    for row in result:

        output += (
            f"{row[0]} | "
            f"{row[1]} {row[2]} | "
            f"{row[3]} | "
            f"{row[4]}\n"
        )

    return output


# ==========================================================
# SEARCH BY STUDENT ID
# ==========================================================

def search_student(student_id):

    query = f"""
    SELECT student_id,
           first_name,
           last_name,
           gender,
           email,
           phone
    FROM warehouse.students
    WHERE student_id='{student_id}';
    """

    result = execute_query(query)

    if not result:
        return "Student not found."

    row = result[0]

    return f"""
🎓 Student Details

Student ID : {row[0]}
Name       : {row[1]} {row[2]}
Gender     : {row[3]}
Email      : {row[4]}
Phone      : {row[5]}
"""


# ==========================================================
# SEARCH BY NAME
# ==========================================================

def search_student_name(name):

    query = f"""
    SELECT student_id,
           first_name,
           last_name
    FROM warehouse.students
    WHERE LOWER(first_name)
    LIKE LOWER('%{name}%');
    """

    result = execute_query(query)

    if not result:
        return "Student not found."

    output = "\n🎓 Matching Students\n"
    output += "-" * 45 + "\n"

    for row in result:
        output += f"{row[0]} | {row[1]} {row[2]}\n"

    return output


# ==========================================================
# GENDER COUNT
# ==========================================================

def gender_count():

    query = """
    SELECT gender,
           COUNT(*)
    FROM warehouse.students
    GROUP BY gender
    ORDER BY gender;
    """

    result = execute_query(query)

    output = "\n👨‍🎓 Student Gender Distribution\n"
    output += "-" * 45 + "\n"

    for row in result:
        output += f"{row[0]} : {row[1]}\n"

    return output


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("STUDENT QUERY MODULE")
    print("=" * 60)

    print("\nTotal Students")
    print(total_students())

    print("\nList Students")
    print(list_students())

    print("\nSearch Student")
    print(search_student("S0001"))

    print("\nSearch Student Name")
    print(search_student_name("Pallavi"))

    print("\nGender Count")
    print(gender_count())