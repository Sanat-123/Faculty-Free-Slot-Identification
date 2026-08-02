"""
---------------------------------------------------------
Attendance Query Module
---------------------------------------------------------
"""

from db import execute_query


# ==========================================================
# OVERALL ATTENDANCE
# ==========================================================

def overall_attendance():

    query = """
    SELECT ROUND(
        100.0 * SUM(CASE WHEN status='Present' THEN 1 ELSE 0 END)
        / COUNT(*), 2)
    FROM warehouse.attendance;
    """

    result = execute_query(query)

    return f"📊 Overall Attendance : {result[0][0]}%"


# ==========================================================
# TOP ATTENDANCE
# ==========================================================

def top_attendance(limit=10):

    query = f"""
    SELECT student_id,
           ROUND(
                100.0 * SUM(CASE WHEN status='Present' THEN 1 ELSE 0 END)
                / COUNT(*),2
           ) AS attendance
    FROM warehouse.attendance
    GROUP BY student_id
    ORDER BY attendance DESC
    LIMIT {limit};
    """

    result = execute_query(query)

    output = "\n🏆 Top Attendance\n"
    output += "-" * 45 + "\n"

    for row in result:
        output += f"{row[0]} : {row[1]}%\n"

    return output


# ==========================================================
# LOW ATTENDANCE
# ==========================================================

def low_attendance(limit=10):

    query = f"""
    SELECT student_id,
           ROUND(
                100.0 * SUM(CASE WHEN status='Present' THEN 1 ELSE 0 END)
                / COUNT(*),2
           ) AS attendance
    FROM warehouse.attendance
    GROUP BY student_id
    ORDER BY attendance ASC
    LIMIT {limit};
    """

    result = execute_query(query)

    output = "\n⚠ Low Attendance\n"
    output += "-" * 45 + "\n"

    for row in result:
        output += f"{row[0]} : {row[1]}%\n"

    return output


# ==========================================================
# STUDENT ATTENDANCE
# ==========================================================

def student_attendance(student_id):

    query = f"""
    SELECT
        student_id,
        ROUND(
            100.0 * SUM(CASE WHEN status='Present' THEN 1 ELSE 0 END)
            / COUNT(*),2
        ) AS attendance
    FROM warehouse.attendance
    WHERE student_id='{student_id}'
    GROUP BY student_id;
    """

    result = execute_query(query)

    if not result:
        return "Student not found."

    row = result[0]

    return f"""
🎓 Student Attendance

Student ID : {row[0]}
Attendance : {row[1]}%
"""


# ==========================================================
# PRESENT / ABSENT SUMMARY
# ==========================================================

def attendance_summary():

    query = """
    SELECT status,
           COUNT(*)
    FROM warehouse.attendance
    GROUP BY status
    ORDER BY status;
    """

    result = execute_query(query)

    output = "\n📈 Attendance Summary\n"
    output += "-" * 40 + "\n"

    for row in result:
        output += f"{row[0]} : {row[1]}\n"

    return output


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("ATTENDANCE QUERY MODULE")
    print("=" * 60)

    print("\nOverall Attendance")
    print(overall_attendance())

    print("\nTop Attendance")
    print(top_attendance())

    print("\nLow Attendance")
    print(low_attendance())

    print("\nStudent Attendance")
    print(student_attendance("S0001"))

    print("\nAttendance Summary")
    print(attendance_summary())