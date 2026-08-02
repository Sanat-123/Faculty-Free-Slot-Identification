import sqlite3
import json
import os

DB_FILE = os.path.join("database", "faculty.db")
JSON_FILE = os.path.join("database", "timetable.json")

connection = sqlite3.connect(DB_FILE)
cursor = connection.cursor()

# ----------------------------
# Delete old table if it exists
# ----------------------------
cursor.execute("DROP TABLE IF EXISTS timetable")

# ----------------------------
# Create fresh table
# ----------------------------
cursor.execute("""
CREATE TABLE timetable(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    teacher TEXT,
    day TEXT,
    slot INTEGER,
    subject TEXT,
    room TEXT,
    class_name TEXT,
    group_name TEXT,
    type TEXT
)
""")

# ----------------------------
# Load JSON
# ----------------------------
with open(JSON_FILE, "r", encoding="utf-8") as file:
    database = json.load(file)

count = 0

# ----------------------------
# Insert Records
# ----------------------------
for teacher, days in database.items():

    for day, lectures in days.items():

        for lecture in lectures:

            cursor.execute("""
            INSERT INTO timetable(
                teacher,
                day,
                slot,
                subject,
                room,
                class_name,
                group_name,
                type
            )
            VALUES(?,?,?,?,?,?,?,?)
            """, (
                teacher,
                day,
                lecture["slot"],
                lecture["subject"],
                lecture["room"],
                lecture["class"],
                lecture["group"],
                lecture["type"]
            ))

            count += 1

connection.commit()
connection.close()

print("Database Created Successfully")
print("Total Records:", count)