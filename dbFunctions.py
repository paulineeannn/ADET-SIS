import sqlite3
from tkinter import messagebox

connection = sqlite3.connect('student-info.db')
cursor = connection.cursor()


def fetchRecord():
    query = "SELECT * FROM student_info"
    cursor.execute(query)
    records = cursor.fetchall()

    return records
def addRecord(studNum, studName, yrSec):
    try: 
        query = "INSERT INTO student_info (studNum, studName, yrSec) VALUES (?, ?, ?);"
        cursor.execute(query, (studNum, studName, yrSec))
        connection.commit()
        messagebox.showinfo("Success", "Student added to the record successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Error creating record: {str(e)}")

def updateRecord(newStudNum, newStudName, newYrSec, oldStudNum):
    try:
        query = "UPDATE student_info SET studNum=?, studName=?, yrSec=? WHERE studNum=?"
        cursor.execute(query, (newStudNum, newStudName, newYrSec, oldStudNum))
        connection.commit()
        messagebox.showinfo("Success", "Record updated successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Error editing record: {str(e)}")

def deleteRecord(studNum):
    try:
        query = "DELETE from student_info WHERE studNum=?"
        cursor.execute(query, (studNum,))
        connection.commit()
        messagebox.showinfo("Success", "Record Deleted successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Error deleting record: {str(e)}")
