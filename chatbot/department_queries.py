"""
---------------------------------------------------------
Department Query Module
---------------------------------------------------------
"""

from db import execute_query


# ==========================================================
# TOTAL DEPARTMENTS
# ==========================================================

def total_departments():

    query = """
    SELECT COUNT(*)
    FROM warehouse.departments;
    """

    return execute_query(query)[0][0]


# ==========================================================
# LIST DEPARTMENTS
# ==========================================================

def list_departments():

    query = """
    SELECT department_id,
           department_name,
           hod_name,
           building
    FROM warehouse.departments
    ORDER BY department_id;
    """

    result = execute_query(query)

    output = "\n🏢 Department List\n"
    output += "-" * 75 + "\n"

    for row in result:

        output += (
            f"{row[0]} | "
            f"{row[1]} | "
            f"HOD : {row[2]} | "
            f"{row[3]}\n"
        )

    return output


# ==========================================================
# SEARCH DEPARTMENT
# ==========================================================

def search_department(name):

    query = f"""
    SELECT department_id,
           department_name,
           hod_name,
           building,
           established_year
    FROM warehouse.departments
    WHERE LOWER(department_name)
    LIKE LOWER('%{name}%');
    """

    result = execute_query(query)

    if not result:
        return "Department not found."

    output = "\n🏢 Department Details\n"
    output += "-" * 60 + "\n"

    for row in result:

        output += (
            f"\nDepartment ID : {row[0]}\n"
            f"Department    : {row[1]}\n"
            f"HOD           : {row[2]}\n"
            f"Building      : {row[3]}\n"
            f"Established   : {row[4]}\n"
        )

    return output


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("DEPARTMENT QUERY MODULE")
    print("=" * 60)

    print("\nTotal Departments")
    print(total_departments())

    print("\nDepartment List")
    print(list_departments())

    print("\nSearch Department")
    print(search_department("Computer"))