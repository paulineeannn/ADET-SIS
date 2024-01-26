import sqlite3

# Connect to SQLite database
connection = sqlite3.connect('student-info.db')
cursor = connection.cursor()

# Create the student_info table with id as the primary key
create_table_query = '''
CREATE TABLE IF NOT EXISTS student_info (
    studNum TEXT PRIMARY KEY CHECK(length(studNum) <= 15),
    studName TEXT NOT NULL,
    yrSec TEXT NOT NULL
);
'''

cursor.execute(create_table_query)

# Commit the changes and close the connection
connection.commit()
connection.close()

print("Database and table created successfully.")
