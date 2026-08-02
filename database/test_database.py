from database.query import execute_query

rows = execute_query("""
SELECT
    teacher,
    day,
    slot,
    subject,
    room,
    class_name,
    group_name,
    type
FROM timetable
LIMIT 30
""")

print("=" * 120)

for row in rows:
    print(row)

print("=" * 120)
print("Rows :", len(rows))