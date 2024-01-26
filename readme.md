# ADET Assignment 
## Pauline Ann P. Bautista
## BSCS 3-5

This contains a simple Student Information System (SIS) implemented in Python using the customtkinter library for the graphical user interface and SQLite for database operations. The system allows users to perform basic CRUD (Create, Read, Update, Delete) operations on student records.

### Files
**1. dbFunctions.py**
This file contains Python functions for interacting with the SQLite database. Functions include fetching records, adding a new student, updating a student record, and deleting a student record.

**2. database.py**
This creates the SQLite database and the student_info table.

**3. gui.py**
It provides different frames for viewing, adding, updating, and deleting student records. The GUI interacts with the database through functions defined in dbFunctions.py.

### Getting Started
1. Ensure you have Python installed on your system.
2. Install the required packages:
- PIL
- customtkinter
- sqlite3
3. Run gui.py to launch the Student Information System:

##Notes:
- The database is initially created by executing database.py. Subsequent executions are not required unless the database structure needs to be reset.
- Images used in the GUI are expected to be in the specified paths (../ADET--SIS/bg.png, ../ADET-SIS/arrow.png). Please ensure these files exist in the specified locations.
