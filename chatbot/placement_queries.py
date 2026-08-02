"""
---------------------------------------------------------
Placement Query Module
---------------------------------------------------------
"""

from db import execute_query


# ==========================================================
# TOTAL COMPANIES
# ==========================================================

def total_companies():

    query = """
    SELECT COUNT(DISTINCT company_name)
    FROM warehouse.placements;
    """

    return execute_query(query)[0][0]


# ==========================================================
# LIST COMPANIES
# ==========================================================

def list_companies():

    query = """
    SELECT DISTINCT company_name
    FROM warehouse.placements
    ORDER BY company_name;
    """

    result = execute_query(query)

    output = "\n💼 Placement Companies\n"
    output += "-" * 45 + "\n"

    count = 1

    for row in result:

        output += f"{count}. {row[0]}\n"

        count += 1

    return output


# ==========================================================
# HIGHEST PACKAGE
# ==========================================================

def highest_package():

    query = """
    SELECT company_name,
           job_role,
           package_lpa
    FROM warehouse.placements
    ORDER BY package_lpa DESC
    LIMIT 1;
    """

    result = execute_query(query)

    row = result[0]

    return f"""
🏆 Highest Package

Company : {row[0]}
Role    : {row[1]}
Package : {row[2]} LPA
"""


# ==========================================================
# AVERAGE PACKAGE
# ==========================================================

def average_package():

    query = """
    SELECT ROUND(AVG(package_lpa),2)
    FROM warehouse.placements;
    """

    result = execute_query(query)

    return f"📈 Average Package : {result[0][0]} LPA"


# ==========================================================
# TOP HIRING COMPANIES
# ==========================================================

def top_companies():

    query = """
    SELECT company_name,
           COUNT(*)
    FROM warehouse.placements
    GROUP BY company_name
    ORDER BY COUNT(*) DESC
    LIMIT 10;
    """

    result = execute_query(query)

    output = "\n🏢 Top Hiring Companies\n"
    output += "-" * 45 + "\n"

    for row in result:

        output += f"{row[0]} : {row[1]} Students\n"

    return output


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("PLACEMENT QUERY MODULE")
    print("=" * 60)

    print("\nTotal Companies")
    print(total_companies())

    print("\nCompany List")
    print(list_companies())

    print("\nHighest Package")
    print(highest_package())

    print("\nAverage Package")
    print(average_package())

    print("\nTop Hiring Companies")
    print(top_companies())