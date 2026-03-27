import requests
import sqlite3

API_URL = "https://openlibrary.org/search.json?q=python+programming&limit=10"

def fetch_books():
    response = requests.get(API_URL, timeout=10)
    response.raise_for_status()
    data = response.json()

    books = []
    for doc in data.get("docs", []):
        books.append({
            "title": doc.get("title", "Unknown"),
            "author": ", ".join(doc.get("author_name", ["Unknown"])),
            "year": doc.get("first_publish_year", None)
        })
    return books

def store_books(books):
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        author TEXT,
        year INTEGER
    )
    """)

    cur.executemany(
        "INSERT INTO books (title, author, year) VALUES (:title, :author, :year)",
        books
    )

    conn.commit()
    conn.close()

def display_books():
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM books")
    rows = cur.fetchall()

    for row in rows:
        print(row)

    conn.close()

if __name__ == "__main__":
    books = fetch_books()
    store_books(books)
    display_books()
