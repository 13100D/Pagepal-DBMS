import sqlite3
import time

# Connect to the SQLite database
conn = sqlite3.connect('pagepal.db')
cursor = conn.cursor()

