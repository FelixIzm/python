import sqlite3
conn = sqlite3.connect("mydatabase.db") # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()
cursor.execute("SELECT count(1) FROM search_ids where flag=0")
count_row = cursor.fetchone()[0]
print(count_row)
