import sqlite3
import os

DB_FILE = os.path.join("database", "faculty.db")


def execute_query(query, parameters=()):

    connection = sqlite3.connect(DB_FILE)

    cursor = connection.cursor()

    cursor.execute(query, parameters)

    rows = cursor.fetchall()

    connection.close()

    return rows