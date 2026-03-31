import sqlite3

conn = sqlite3.connect("smartcrop.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM diseases")
rows = cursor.fetchall()

print("Total Rows:", len(rows))   # 👈 ye add karo

for row in rows:
    print(row)

conn.close()