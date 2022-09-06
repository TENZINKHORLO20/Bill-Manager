import os
from pickle import FALSE
import sqlite3

try:
    os.remove("bill_management.db")
    print("bill_management.db removed successfully!")
except OSError as error:
    print("No file month.db found >> Proceeding")

conn = sqlite3.connect('bill_management.db')
c = conn.cursor()

c.execute('PRAGMA foreign_keys=ON')
conn.commit()

c.execute("""CREATE TABLE month (
    mid INTEGER PRIMARY KEY NOT NULL,
    month TEXT,
    completed BOOLEAN)""")

conn.commit()

monthlist = [
    (1,"January",False),
    (2,"Febuary",False),
    (3,"March",False),
    (4,"April",False),
    (5,"May",False),
    (6,"June",False),
    (7,"July",False),
    (8,"August",False),
    (9,"September",False),
    (10,"October",False),
    (11,"November",False),
    (12,"December",False)
]

c.executemany("INSERT INTO month VALUES (?,?,?)",monthlist)
conn.commit()

c.execute("""CREATE TABLE bills (
    billid TEXT PRIMARY KEY NOT NULL,
    mid INTEGER NOT NULL,
    item TEXT NOT NULL,
    price REAL NOT NULL,
    FOREIGN KEY (mid) REFERENCES month(mid))""")

conn.commit()


conn.close()