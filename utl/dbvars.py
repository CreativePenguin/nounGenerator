import sqlite3

DB_FILE = "Info.db"
db = sqlite3.connect(DB_FILE)

db_cursor = db.cursor()
