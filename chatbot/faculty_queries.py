"""
---------------------------------------------------------
Faculty Query Module
---------------------------------------------------------
"""

from db import execute_query


# ==========================================================
# TOTAL FACULTY
# ==========================================================

def total_faculty():

    query = """
    SELECT COUNT(*)
    FROM warehouse.faculty;
    """

    return execute_query(query)[0][0]


# ==========================================================
# LIST FACULTY
# ==========================================================

def list_faculty(limit=10):

    query = f"""
    SELECT faculty_id,
           faculty_name,
           designation
    FROM warehouse.faculty
    ORDER BY faculty_id
    LIMIT {limit};
    """

    result = execute_query(query)

    if not result:
        return "No faculty found."

    output = "\n👨‍🏫 Faculty List\n"
    output += "-" * 70 + "\n"

    for row in result:

        output += (
            f"{row[0]} | "
            f"{row[1]} | "
            f"{row[2]}\n"
        )

    return output


# ==========================================================
# SEARCH FACULTY
# ==========================================================

def search_faculty(name):

    query = f"""
    SELECT faculty_id,
           faculty_name,
           designation,
           email,
           experience
    FROM warehouse.faculty
    WHERE LOWER(faculty_name)
    LIKE LOWER('%{name}%');
    """

    result = execute_query(query)

    if not result:
        return "Faculty not found."

    output = "\n👨‍🏫 Faculty Details\n"
    output += "-" * 60 + "\n"

    for row in result:

        output += (
            f"\nFaculty ID : {row[0]}\n"
            f"Name       : {row[1]}\n"
            f"Designation: {row[2]}\n"
            f"Email      : {row[3]}\n"
            f"Experience : {row[4]} Years\n"
        )

    return output


# ==========================================================
# FACULTY DESIGNATION SUMMARY
# ==========================================================

def faculty_designations():

    query = """
    SELECT designation,
           COUNT(*)
    FROM warehouse.faculty
    GROUP BY designation
    ORDER BY designation;
    """

    result = execute_query(query)

    output = "\n📊 Faculty Designation Summary\n"
    output += "-" * 45 + "\n"

    for row in result:
        output += f"{row[0]} : {row[1]}\n"

    return output


# ==========================================================
# TEST MODULE
# ==========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("FACULTY QUERY MODULE")
    print("=" * 60)

    print("\nTotal Faculty")
    print(total_faculty())

    print("\nFaculty List")
    print(list_faculty())

    print("\nSearch Faculty")
    print(search_faculty("Peter"))

    print("\nDesignation Summary")
    print(faculty_designations())