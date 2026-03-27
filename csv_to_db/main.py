import csv
import sqlite3

def import_csv():
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    with open("users.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        columns = reader.fieldnames

        col_defs = "id INTEGER PRIMARY KEY AUTOINCREMENT, " + \
                   ", ".join(f'"{c}" TEXT' for c in columns)

        cur.execute(f"CREATE TABLE IF NOT EXISTS users ({col_defs})")

        placeholders = ", ".join("?" * len(columns))
        col_names = ", ".join(columns)

        for row in reader:
            values = [row[c] for c in columns]
            cur.execute(
                f"INSERT INTO users ({col_names}) VALUES ({placeholders})",
                values
            )

    conn.commit()
    conn.close()

if __name__ == "__main__":
    import_csv()
