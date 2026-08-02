"""
---------------------------------------------------------
Library Query Module
---------------------------------------------------------
"""

from db import execute_query


# ==========================================================
# TOTAL BOOKS
# ==========================================================

def total_books():

    query = """
    SELECT COUNT(*)
    FROM warehouse.library_books;
    """

    return execute_query(query)[0][0]


# ==========================================================
# LIST BOOKS
# ==========================================================

def list_books(limit=10):

    query = f"""
    SELECT book_id,
           book_name,
           author,
           publisher
    FROM warehouse.library_books
    ORDER BY book_id
    LIMIT {limit};
    """

    result = execute_query(query)

    if not result:
        return "No books found."

    output = "\n📚 Library Books\n"
    output += "-" * 90 + "\n"

    for row in result:

        output += (
            f"{row[0]} | "
            f"{row[1]} | "
            f"{row[2]} | "
            f"{row[3]}\n"
        )

    return output


# ==========================================================
# SEARCH BOOK
# ==========================================================

def search_book(book_name):

    query = f"""
    SELECT book_id,
           book_name,
           author,
           publisher,
           publication_year
    FROM warehouse.library_books
    WHERE LOWER(book_name)
    LIKE LOWER('%{book_name}%');
    """

    result = execute_query(query)

    if not result:
        return "Book not found."

    output = "\n📖 Search Results\n"
    output += "-" * 90 + "\n"

    for row in result:

        output += (
            f"\nBook ID          : {row[0]}\n"
            f"Book Name        : {row[1]}\n"
            f"Author           : {row[2]}\n"
            f"Publisher        : {row[3]}\n"
            f"Publication Year : {row[4]}\n"
        )

    return output


# ==========================================================
# BOOKS BY PUBLISHER
# ==========================================================

def books_by_publisher():

    query = """
    SELECT publisher,
           COUNT(*)
    FROM warehouse.library_books
    GROUP BY publisher
    ORDER BY COUNT(*) DESC;
    """

    result = execute_query(query)

    output = "\n🏢 Books by Publisher\n"
    output += "-" * 45 + "\n"

    for row in result:

        output += f"{row[0]} : {row[1]} Books\n"

    return output


# ==========================================================
# SEARCH BY AUTHOR
# ==========================================================

def search_author(author):

    query = f"""
    SELECT book_id,
           book_name,
           author,
           publisher
    FROM warehouse.library_books
    WHERE LOWER(author)
    LIKE LOWER('%{author}%');
    """

    result = execute_query(query)

    if not result:
        return "Author not found."

    output = "\n✍ Books by Author\n"
    output += "-" * 90 + "\n"

    for row in result:

        output += (
            f"{row[0]} | "
            f"{row[1]} | "
            f"{row[2]} | "
            f"{row[3]}\n"
        )

    return output


# ==========================================================
# TEST MODULE
# ==========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("LIBRARY QUERY MODULE")
    print("=" * 60)

    print("\nTotal Books")
    print(total_books())

    print("\nBook List")
    print(list_books())

    print("\nSearch Book")
    print(search_book("Python"))

    print("\nBooks by Publisher")
    print(books_by_publisher())

    print("\nSearch Author")
    print(search_author("John"))