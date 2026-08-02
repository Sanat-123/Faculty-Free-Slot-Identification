from database.query import execute_query
from knowledge.subjects import SUBJECTS

rows = execute_query("""

SELECT DISTINCT subject
FROM timetable
ORDER BY subject

""")

for row in rows:

    SUBJECTS.add(row[0])

print()

print("Subjects :", len(SUBJECTS))

print()

for subject in sorted(SUBJECTS):

    print(subject)