import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Read CSV
df = pd.read_csv("data.csv")

# Step 2: Calculate average
df["average"] = df[["math", "science", "english"]].mean(axis=1)

# Step 3: Connect to SQLite
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

# Step 4: Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    name TEXT,
    math INTEGER,
    science INTEGER,
    english INTEGER,
    average REAL
)
""")

# Step 5: Insert data
df.to_sql("students", conn, if_exists="replace", index=False)

# Step 6: Fetch data
data = pd.read_sql("SELECT * FROM students", conn)

print("\nStored Data:\n", data)

# Step 7: Plot graph
plt.bar(data["name"], data["average"])
plt.title("Student Average Scores")
plt.xlabel("Students")
plt.ylabel("Average Score")
plt.show()

# Close connection
conn.close()
