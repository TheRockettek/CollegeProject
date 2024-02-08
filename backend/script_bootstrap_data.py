""" Script to load the bootstrap data into the database. """

from queries import conn

# Bootstrap data
with open("bootstrap_data.sql", "r", encoding="utf-8") as file:
    conn.executescript(file.read())

print("Bootstrap data loaded successfully.")
