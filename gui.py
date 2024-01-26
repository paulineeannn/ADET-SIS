import customtkinter as ctk
from tkinter import messagebox, ttk
from PIL import Image
from dbFunctions import *

frameCreate = None
frameRead = None
frameUpdate = None
frameDelete = None

def displayHome():
    if frameCreate != None:
        frameCreate.destroy()
    elif frameRead != None:
        frameRead.destroy()
    elif frameUpdate != None :
        frameUpdate.destroy()
    elif frameDelete != None :
        frameDelete.destroy()

    global frameHome
    frameHome = ctk.CTkFrame(window, width=900, height=600, fg_color="#810000")
    frameHome.pack()

    imgBg = ctk.CTkImage(light_image=Image.open("../ADET-SIS/bg.png"), size=(900, 600))

    labelBg = ctk.CTkLabel(frameHome, image=imgBg, text="")
    labelBg.place(x=0, y=0)

    buttonTexts = ["View Records", "Add New Student", "Edit Student Record", "Delete Record"]
    buttonCommands = [displayView, displayCreate, displayUpdate, displayDelete]

    y = 260
    for x in range(len(buttonTexts)):
        button = ctk.CTkButton(frameHome, text=buttonTexts[x], font=("Arial", 18, "bold"),
                               width=275, height=50, fg_color="#FFFFFF", text_color="#810000", hover_color="#D0ABA7",
                               command=buttonCommands[x])
        button.place(x=312, y=y)
        y += 65

def displayCreate():
    def submit():
        studNum = entrystudNum.get()
        studName = entryName.get()
        yrSec = entryYrSec.get()

        if len(studNum) == 15 :
            addRecord(studNum, studName, yrSec)
            frameCreate.destroy()
            displayCreate()
        else:
            messagebox.showerror("Failed", f"Student number must be exactly 15 characters")

    frameHome.destroy()

    global frameCreate
    frameCreate = ctk.CTkFrame(window, width=900, height=600, fg_color="#810000")
    frameCreate.place(x=0, y=0)

    frameForm = ctk.CTkFrame(frameCreate, width=716, height=380)
    frameForm.place(x=92, y=122)
    
    labelHeading = ctk.CTkLabel(frameCreate, text="ADD NEW STUDENT", font=("Arial", 40, "bold"), text_color="#FFFFFF",  width=780, justify="center")
    labelHeading.place(x=60, y=50)


    buttonBack = ctk.CTkButton(frameCreate, text="⬅", font=("Arial", 30), command=displayHome, fg_color="transparent", hover_color="#810000")
    buttonBack.place(x=0, y=30)

    labelstudNum = ctk.CTkLabel(frameForm, text="Student Number:", font=("Arial", 24, "bold"), text_color="#810000")
    labelstudNum.place(x=22, y=21)
    entrystudNum = ctk.CTkEntry(frameForm, font=("Arial", 24), text_color="#810000", width=550, height=47)
    entrystudNum.place(x=22, y=54)

    labelName = ctk.CTkLabel(frameForm, text="Name:", font=("Arial", 24, "bold"), text_color="#810000")
    labelName.place(x=22, y=118)
    entryName = ctk.CTkEntry(frameForm, font=("Arial", 24), text_color="#810000", width=670, height=47)
    entryName.place(x=22, y=151)

    labelYrSec = ctk.CTkLabel(frameForm, text="Year and Section:", font=("Arial", 24, "bold"), text_color="#810000")
    labelYrSec.place(x=22, y=216)
    entryYrSec = ctk.CTkEntry(frameForm, font=("Arial", 24), text_color="#810000", width=370, height=47)
    entryYrSec.place(x=22, y=249)

    buttonSubmit = ctk.CTkButton(frameForm, text="Submit", font=("Arial", 24), fg_color="#810000", hover_color="#590000", width=275, height=47, command=submit)
    buttonSubmit.place(x=236, y=315)

def createTree(frame):
    try:
        records = fetchRecord()
        
        if not records:
            messagebox.showinfo("Info", "No records found.")
        else:
            # Create a style object
            style = ttk.Style()

            # Configure the style properties for the heading
            style.configure("Custom.Treeview.Heading",
                            font=("Arial", 15, "bold"))

            # Configure the Treeview widget style
            style.configure("Custom.Treeview",
                            font=("Arial", 13),
                            rowheight=30)

            # Create a Treeview widget
            tree = ttk.Treeview(frame, style="Custom.Treeview", columns=("Student Number", "Name", "Year and Section"), show="headings")
            tree.heading("Student Number", text="Student Number")
            tree.column("Student Number", minwidth=280, width=335)
            tree.heading("Name", text="Name")
            tree.column("Name", minwidth=280, width=335)
            tree.heading("Year and Section", text="Year and Section")
            tree.column("Year and Section", minwidth=300, width=300)

            # Insert records into the Treeview
            for record in records:
                tree.insert("", "end", values=(record[0], record[1], record[2]))

            tree['height'] = 12

            return tree

    except Exception as e:
        messagebox.showerror("Error", f"Error reading records: {str(e)}")

def displayView():
    frameHome.destroy()

    global frameRead
    frameRead = ctk.CTkFrame(window, width=900, height=600, fg_color="#810000")
    frameRead.place(x=0, y=0)

    labelHeading = ctk.CTkLabel(frameRead, text="VIEW STUDENT RECORDS", font=("Arial", 40, "bold"),
                                text_color="#FFFFFF", width=780, justify="center")
    labelHeading.place(x=60, y=50)

    buttonBack = ctk.CTkButton(frameRead, text="⬅", font=("Arial", 30), command=displayHome, fg_color="transparent", hover_color="#810000")
    buttonBack.place(x=0, y=30)

    tree = createTree(frameRead)
    tree.place(x=70, y=142)

def displayUpdate():
    def update():
        selectedRow = treeUpdate.focus()
        studentInfos = treeUpdate.item(selectedRow)['values']
        oldStudNum = studentInfos[0]
        oldStudName = studentInfos[1]
        oldYrSec = studentInfos[2]

        frameUpdate.destroy()

        global frameEditRecord
        frameEditRecord = ctk.CTkFrame(window, width=900, height=600, fg_color="#810000")
        frameEditRecord.place(x=0, y=0)

        frameEditForm = ctk.CTkFrame(frameEditRecord, width=715, height=380)
        frameEditForm.place(x=92, y=142)

        def commandBack():
            frameEditForm.destroy()
            displayUpdate()

        buttonBack = ctk.CTkButton(frameEditRecord, text="⬅", font=("Arial", 30), command=commandBack, fg_color="transparent", hover_color="#810000")
        buttonBack.place(x=0, y=30)

        def updateSQLite():
            newName = entryName.get()
            newYrSec = entryYrSec.get()
            newStudNum = entrystudNum.get()

            try:
                updateRecord(newStudNum, newName, newYrSec, oldStudNum)
                frameEditForm.destroy()
                displayUpdate()
            except Exception as e:
                messagebox.showerror("Error", f"Error updating record: {str(e)}")

        labelHeading = ctk.CTkLabel(frameEditRecord, text="EDIT STUDENT RECORD", font=("Arial", 50, "bold"),
                                    text_color="#FFFFFF", width=780, justify="center")
        labelHeading.place(x=60, y=80)

        labelstudNum = ctk.CTkLabel(frameEditForm, text="Student Number:", font=("Arial", 24, "bold"), text_color="#810000")
        labelstudNum.place(x=22, y=21)
        entrystudNum = ctk.CTkEntry(frameEditForm, font=("Arial", 24), text_color="#810000", width=550, height=47)
        entrystudNum.place(x=22, y=54)
        entrystudNum.insert(0, oldStudNum)

        labelName = ctk.CTkLabel(frameEditForm, text="Name:", font=("Arial", 24, "bold"), text_color="#810000")
        labelName.place(x=22, y=118)
        entryName = ctk.CTkEntry(frameEditForm, font=("Arial", 24), text_color="#810000", width=670, height=47)
        entryName.place(x=22, y=151)
        entryName.insert(0, oldStudName)

        labelYrSec = ctk.CTkLabel(frameEditForm, text="Year and Section:", font=("Arial", 24, "bold"),
                                  text_color="#810000")
        labelYrSec.place(x=22, y=216)
        entryYrSec = ctk.CTkEntry(frameEditForm, font=("Arial", 24), text_color="#810000", width=370, height=47)
        entryYrSec.place(x=22, y=249)
        entryYrSec.insert(0, oldYrSec)


        buttonSubmit = ctk.CTkButton(frameEditForm, text="Submit", font=("Arial", 24), text_color="#FFFFFF", fg_color="#810000", hover_color="#590000", width=275,
                                     height=47, command=updateSQLite)
        buttonSubmit.place(x=236, y=315)

    frameHome.destroy()

    global frameUpdate
    frameUpdate = ctk.CTkFrame(window, width=900, height=600, fg_color="#810000")
    frameUpdate.place(x=0, y=0)

    labelHeading = ctk.CTkLabel(frameUpdate, text="EDIT STUDENT RECORD", font=("Arial", 40, "bold"), text_color="#FFFFFF",  width=780, justify="center")
    labelHeading.place(x=60, y=50)

    buttonBack = ctk.CTkButton(frameUpdate, text="⬅", font=("Arial", 30), command=displayHome, fg_color="transparent", hover_color="#810000")
    buttonBack.place(x=0, y=30)

    treeUpdate = createTree(frameUpdate)
    treeUpdate.place(x=70, y=142)

    buttonEdit = ctk.CTkButton(frameUpdate, text="Edit", font=("Arial", 24),
                               text_color="#810000", fg_color="#FFFFFF", hover_color="#D0ABA7",
                               width=275, height=47, command=update)
    buttonEdit.place(x=328, y=480)

    
def displayDelete():
    def delete():
        selectedRow = tree.focus()
        studentInfos = tree.item(selectedRow)['values']
        studNum = studentInfos[0]
        deleteRecord(studNum)
        frameDelete.destroy()
        displayDelete()

    frameHome.destroy()

    global frameDelete
    frameDelete = ctk.CTkFrame(window, width=900, height=600, fg_color="#810000")
    frameDelete.place(x=0, y=0)

    labelHeading = ctk.CTkLabel(frameDelete, text="SELECT STUDENT TO DELETE", font=("Arial", 40, "bold"), text_color="#FFFFFF",  width=780, justify="center")
    labelHeading.place(x=60, y=50)

    buttonBack = ctk.CTkButton(frameDelete, text="⬅", font=("Arial", 30), command=displayHome, fg_color="transparent", hover_color="#810000")
    buttonBack.place(x=0, y=30)

    tree = createTree(frameDelete)
    tree.place(x=70, y=142)

    buttonDelete = ctk.CTkButton(frameDelete, text="Delete", font=("Arial", 24),
                               text_color="#810000", fg_color="#FFFFFF", hover_color="#D0ABA7",
                               width=275, height=47, command=delete)
    buttonDelete.place(x=328, y=480)
    

window = ctk.CTk(fg_color="#810000")
window.title("Student Information System")

# get the user's screen size
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Calculate the center coordinates
center_x = int((screen_width - 900) // 2)
center_y = int((screen_height - 600) // 2)

window.geometry("900x600+{}+{}".format(center_x, center_y))
window.resizable(0, 0)


displayHome()

window.mainloop()
