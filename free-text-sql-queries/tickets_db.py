from datetime import date, timedelta
import sqlite3
import pandas as pd

# Connect to the SQLite database
connection = sqlite3.connect('tickets.db')

# Create a cursor object
cursor = connection.cursor()

create_tables_query = ['''
-- Create the 'author' table if it doesn't exist
CREATE TABLE IF NOT EXISTS author (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);''',
'''-- Create the 'ticket' table if it doesn't exist
CREATE TABLE IF NOT EXISTS ticket (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT NOT NULL CHECK (status IN ('Open', 'Closed', 'Under Investigation'))  ,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    closed_at DATETIME,
    author_id INTEGER,
    FOREIGN KEY (author_id) REFERENCES author (id)
);''',
'''
-- Create the 'comment' table if it doesn't exist
CREATE TABLE IF NOT EXISTS comment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    comment TEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    author_id INTEGER,
    ticket_id INTEGER,
    FOREIGN KEY (author_id) REFERENCES author (id),
    FOREIGN KEY (ticket_id) REFERENCES ticket (id)
);''',
'''
-- Add index to 'ticket_id' in 'comment' table for better performance
-- Check if the index already exists before creating it
CREATE INDEX IF NOT EXISTS idx_ticket_id ON comment(ticket_id);
''']

def createDb():
    for q in create_tables_query:
        cursor.execute(q)

def populateDb():
    authors = [(1, "John"), (2, "melanie"), (3, "Jane"), (4, "Alice"), (5, "Frank")]
    insert_authors = "INSERT INTO author (id, name) values (?, ?);"
    cursor.executemany(insert_authors, authors)
    tickets = [
        (1, "ticket 1", "description ticket 1", "Open", date.today() - timedelta(5), None, 1),
        (2, "ticket 2", "description ticket 2", "Under Investigation", date.today() - timedelta(5), None, 2),
        (3, "ticket 3", "description ticket 3", "Open", date.today() - timedelta(5), None, 3),
        (4, "ticket 4", "description ticket 4", "Closed", date.today() - timedelta(5), date.today() - timedelta(4), 1),
        (5, "ticket 5", "description ticket 5", "Closed", date.today() - timedelta(5), date.today() - timedelta(3), 1),
        (6, "ticket 6", "description ticket 6", "Open", date.today() - timedelta(5), None, 1),
        (7, "ticket 7", "description ticket 7", "Open", date.today() - timedelta(5), None, 4),
        (8, "ticket 8", "description ticket 8", "Under Investigation", date.today() - timedelta(5), None, 1),
        (9, "ticket 9", "description ticket 9", "Open", date.today() - timedelta(5), None, 1),
        (10, "ticket 10", "description ticket 10", "Open", date.today() - timedelta(5), None, 1),     
    ]
    insert_tickets = "INSERT INTO ticket (id, title, description, status, created_at, closed_at, author_id) VALUES (?, ?, ?, ?, ?, ?, ? );"
    cursor.executemany(insert_tickets, tickets)
    comments = [
        (1, "comment 1", date.today() - timedelta(4), 5, 2),
        (2, "comment 2", date.today() - timedelta(4), 1, 2),
        (3, "comment 3", date.today() - timedelta(3), 1, 2),
        (4, "comment 4", date.today() - timedelta(3), 2, 2),
        (5, "comment 5", date.today() - timedelta(4), 3, 4),
        (6, "comment 6", date.today() - timedelta(4), 5, 5),
        (7, "comment 7", date.today() - timedelta(4), 5, 5)
    ]
    insert_comments = "INSERT INTO comment (id, comment, created_at, author_id, ticket_id) values (?, ?, ?, ?, ?);"
    cursor.executemany(insert_comments, comments)
    connection.commit()

def runQueryAndReturnDF(query):
    connection = sqlite3.connect('tickets.db')
    return pd.read_sql_query(query,  connection)
    # cursor = connection.execute(query)

    # rows = cursor.fetchall()
    # columns = [col[0] for col in cursor.description]
    # return [dict(zip(columns, row)) for row in rows]


if __name__ == "__main__":
    createDb()
    populateDb()
