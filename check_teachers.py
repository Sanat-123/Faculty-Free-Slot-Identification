import sqlite3
import os

DB_FILE = os.path.join("database", "faculty.db")

connection = sqlite3.connect(DB_FILE)
cursor = connection.cursor()

cursor.execute("""
SELECT teacher, COUNT(*)
FROM timetable
GROUP BY teacher
ORDER BY teacher
""")

rows = cursor.fetchall()

for teacher, count in rows:
    print(f"{teacher} --> {count}")
connection.close()