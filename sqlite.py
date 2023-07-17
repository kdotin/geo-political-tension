import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('articles.db')
c = conn.cursor()

# Query the database
c.execute("SELECT * FROM articles")

# Fetch all the rows
rows = c.fetchall()

# Print each row
for row in rows:
    print(f"Headline: {row[0]}")
    print(f"URL: {row[1]}")
    print(f"Content: {row[2]}\n\n")

# Close the connection to the database
conn.close()
