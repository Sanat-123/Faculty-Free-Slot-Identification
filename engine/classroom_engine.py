import sqlite3
import os

DB_FILE = os.path.join("database", "faculty.db")


def find_busy_rooms(day, slot):

    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT DISTINCT room
        FROM timetable
        WHERE day = ?
        AND slot = ?
        AND room != ''
        ORDER BY room
    """, (day, slot))

    rooms = [row[0] for row in cursor.fetchall()]

    connection.close()

    return rooms


print("=" * 60)
print("BUSY CLASSROOM SEARCH")
print("=" * 60)

day = input("Enter Day : ").strip()

slot = int(input("Enter Slot : "))

rooms = find_busy_rooms(day, slot)

print("\nBusy Rooms\n")

for room in rooms:
    print(room)

print("\nTotal Busy Rooms:", len(rooms))