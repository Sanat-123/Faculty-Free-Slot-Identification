"""
---------------------------------------------------------
University Analytics Chatbot
Database Connection Module
---------------------------------------------------------
Author : Sanat Agarwal
Project : University Data Engineering Platform
---------------------------------------------------------
"""

import psycopg2

# ==========================================================
# DATABASE CONFIGURATION
# ==========================================================

DB_HOST = "localhost"
DB_NAME = "university_dw"
DB_USER = "postgres"
DB_PASSWORD = "postgres123"
DB_PORT = "5432"


# ==========================================================
# DATABASE CONNECTION
# ==========================================================

def get_connection():
    """
    Creates and returns PostgreSQL database connection.
    """

    try:

        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )

        return conn

    except Exception as e:

        print("\n❌ Database Connection Error")
        print(e)

        return None


# ==========================================================
# COMMON QUERY EXECUTION FUNCTION
# ==========================================================

def execute_query(query):
    """
    Executes a SELECT query and returns all rows.
    """

    conn = get_connection()

    if conn is None:
        return None

    cursor = conn.cursor()

    try:

        cursor.execute(query)

        result = cursor.fetchall()

        cursor.close()
        conn.close()

        return result

    except Exception as e:

        print("\n❌ Query Execution Error")
        print(e)

        cursor.close()
        conn.close()

        return None


# ==========================================================
# TEST CONNECTION
# ==========================================================

def test_connection():

    conn = get_connection()

    if conn is None:
        print("\n❌ Connection Failed!")
        return

    cursor = conn.cursor()

    cursor.execute("SELECT current_database();")

    db_name = cursor.fetchone()[0]

    print("=" * 60)
    print("🎉 Connected Successfully!")
    print("Database :", db_name)
    print("=" * 60)

    cursor.close()
    conn.close()


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":
    test_connection()