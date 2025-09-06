import tkinter as tk
import re
from tkinter import messagebox
from tkinter import *
from datetime import datetime
import mysql.connector

#connect to mysql
conn=mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="students_db"
)
cursor=conn.cursor()

#functions in DB

def submit_student():
     #Basic required fields

    if first_name.get() == "" or last_name.get() == "":
        messagebox.showerror("Error", "First Name and Last Name are required")
        return

     # Validate Year
    if not year.get().isdigit():
        messagebox.showerror("Error", "Year must be a number")
        return
    
    # Validate Age 
    if not age.get().isdigit():
        messagebox.showerror("Error", "Age must be a number")
        return

    # Validate Mobile Number
    if not (mobile_no.get().isdigit() and len(mobile_no.get()) == 10):
        messagebox.showerror("Error", "Mobile number must be exactly 10 digits")
        return

    # Validate Email
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}$'
    if not re.match(email_pattern, email_id.get()):
        messagebox.showerror("Error", "Invalid Email Address")
        return

     # Validate DOB
    dob = date_of_birth.get().strip()
    try:
            # User gives DD/MM/YYYY → convert to YYYY-MM-DD
            dob_mysql = datetime.strptime(dob, "%d/%m/%Y").strftime("%Y-%m-%d")
    except ValueError:
            messagebox.showerror("Error", "Date must be in DD/MM/YYYY format (e.g., 02/05/1990)")
            return 
    '''try:
        dob = datetime.strptime(date_of_birth.get(), "%d/%m/%Y")  # must be DD/MM/YYYY
        if dob > datetime.now():
            messagebox.showerror("Error", "Date of Birth cannot be in the future")
            return
    except ValueError:
        messagebox.showerror("Error", "Invalid Date of Birth format. Use DD/MM/YYYY")
        return'''
    
    sql="""INSERT INTO students(first_name,last_name,course,subject_name,year,age,gender,date_of_birth,mobile_no,email_id,location)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    values=(first_name.get(),
            last_name.get(),
            course.get(),
            subject_name.get(),
            int (year.get()),
            int (age.get()),gender.get(),
            dob_mysql,# MySQL expects YYYY-MM-DD format
            mobile_no.get(),
            email_id.get(),
            location.get())
    cursor.execute(sql,values)
    conn.commit()
    messagebox.showinfo("Success","student added successfully!")
    clear_form() #clear after submit
    

def enable_student_id():
    student_id.config(state="normal")  # Enable for input
    student_id.delete(0, tk.END)
    student_id.focus()  

def add_new():
    # clear all entry fields
    
    first_name.delete(0, tk.END)
    last_name.delete(0, tk.END)
    course.delete(0, tk.END)
    subject_name.delete(0, tk.END)
    year.delete(0, tk.END)
    age.delete(0, tk.END)
    gender.delete(0, tk.END)
    date_of_birth.delete(0, tk.END)
    mobile_no.delete(0, tk.END)
    email_id.delete(0, tk.END)
    location.delete(0,tk.END)
    # Disable Student ID so user can't type
    student_id.config(state="disabled")
    student_id.delete(0,tk.END)
    messagebox.showinfo("New Entry", "Form is ready for new student details!")

def view_students():
    student_id.config(state="normal")
    sid = student_id.get().strip()       # from Entry box
    fname = first_name.get().strip()     # from Entry box

    if sid:  # Search by ID
        query = "SELECT * FROM students WHERE id = %s"
        cursor.execute(query, (sid,))
    elif fname:  # Search by Name
        query = "SELECT * FROM students WHERE first_name = %s"
        cursor.execute(query, (fname,))
    else:  # If nothing entered, show all
        query = "SELECT * FROM students"
        cursor.execute(query)

    rows = cursor.fetchall()
    output = "\n".join(str(row) for row in rows)
    messagebox.showinfo("Students Records", output if output else "No records found.")

def delete_student():
    student_id.config(state="normal")
    sid = student_id.get().strip()
    if not sid:
        messagebox.showerror("Error", "Enter Student ID to delete record")
        return
    sql = "DELETE FROM students WHERE id=%s"
    cursor.execute(sql, (sid,))
    conn.commit()
    messagebox.showinfo("Deleted", "Student record deleted successfully!")

# ===== UPDATE Function ===== 
def update_student():
    student_id.config(state="normal")
    sid = student_id.get().strip()
    if not sid:
        messagebox.showerror("Error", "Please enter a valid Student ID to update")
        return

    update_fields = []
    values = []

    # First Name
    if first_name.get().strip():
        update_fields.append("first_name=%s")
        values.append(first_name.get().strip())

    # Last Name
    if last_name.get().strip():
        update_fields.append("last_name=%s")
        values.append(last_name.get().strip())

    # Course
    if course.get().strip():
        update_fields.append("course=%s")
        values.append(course.get().strip())

    # Subject Name
    if subject_name.get().strip():
        update_fields.append("subject_name=%s")
        values.append(subject_name.get().strip())

    # Year (validate only if provided)
    if year.get().strip():
        if not year.get().isdigit():
            messagebox.showerror("Error", "Year must be a number")
            return
        update_fields.append("year=%s")
        values.append(int(year.get()))

    # Age
    if age.get().strip():
        if not age.get().isdigit():
            messagebox.showerror("Error", "Age must be a number")
            return
        update_fields.append("age=%s")
        values.append(int(age.get()))

    # Gender
    if gender.get().strip():
        update_fields.append("gender=%s")
        values.append(gender.get().strip())

    # Date of Birth
    if date_of_birth.get().strip():
        dob = date_of_birth.get().strip()
        try:
            dob_mysql = datetime.strptime(dob, "%d/%m/%Y").strftime("%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid Date of Birth format. Use DD/MM/YYYY")
            return
        update_fields.append("date_of_birth=%s")
        values.append(dob_mysql)

    # Mobile Number
    if mobile_no.get().strip():
        if not (mobile_no.get().isdigit() and len(mobile_no.get()) == 10):
            messagebox.showerror("Error", "Mobile number must be exactly 10 digits")
            return
        update_fields.append("mobile_no=%s")
        values.append(mobile_no.get().strip())

    # Email
    if email_id.get().strip():
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}$'
        if not re.match(email_pattern, email_id.get()):
            messagebox.showerror("Error", "Invalid Email Address")
            return
        update_fields.append("email_id=%s")
        values.append(email_id.get().strip())

    # Location
    if location.get().strip():
        update_fields.append("location=%s")
        values.append(location.get().strip())

    if not update_fields:
        messagebox.showwarning("No Update", "No fields provided to update")
        return

    # Build SQL dynamically
    sql = "UPDATE students SET " + ", ".join(update_fields) + " WHERE id=%s"
    values.append(sid)

    try:
        cursor.execute(sql, values)
        conn.commit()
        messagebox.showinfo("Success", "Student record updated successfully!")
        clear_form() 
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")

# ===== CLEAR Function =====
def clear_form():
    student_id.delete(0,tk.END)
    first_name.delete(0, tk.END)
    last_name.delete(0, tk.END)
    course.delete(0, tk.END)
    subject_name.delete(0, tk.END)
    year.delete(0, tk.END)
    age.delete(0, tk.END)
    gender.delete(0, tk.END)
    date_of_birth.delete(0, tk.END)
    mobile_no.delete(0, tk.END)
    email_id.delete(0, tk.END)
    location.delete(0,tk.END)
    messagebox.showinfo("Info", "Form cleared!.")


# ===== EXIT Function =====
def exit_app():
    if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
        window.destroy()



#GUI
    
window=tk.Tk()
window.title("PYTHON PROJECT")
window.geometry("900x600")

window.rowconfigure(0, weight=0)   # heading row (fixed height)
window.rowconfigure(1, weight=1)   # content row (expandable)
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)
window.protocol("WM_DELETE_WINDOW", exit_app)

# Heading Label (row=0, spans across 2 columns)
label = tk.Label(window, text="Student Management System",font=("Arial", 20, "bold"), fg="white", bg="black")
label.grid(row=0, column=0, columnspan=2, sticky="nsew")

# Left Frame
left_frame = tk.Frame(window, bg="deepskyblue", width=400, height=300)
left_frame.grid(row=1, column=0, sticky="nsew")

# Right Frame
right_frame = tk.Frame(window, bg="lightgray", width=100, height=300)
right_frame.grid(row=1, column=1, sticky="nsew")

#add label in left frame
#first row

tk.Label(left_frame, text="First Name", bg="deepskyblue", fg="black", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5, pady=0, sticky="w")
first_name = tk.Entry(left_frame,width=35)
first_name.grid(row=1, column=0,padx=6, pady=0)

tk.Label(left_frame, text="Last Name", bg="deepskyblue", fg="black", font=("Arial", 12, "bold")).grid(row=0, column=5, padx=0, pady=0, sticky="w")
last_name = tk.Entry(left_frame,width=35)
last_name.grid(row=1, column=5, padx=0, pady=0)

# Second row
tk.Label(left_frame, text="Course", bg="deepskyblue", fg="black", font=("Arial", 12, "bold")).grid(row=2, column=0, padx=5, pady=0, sticky="w")
course = tk.Entry(left_frame, width=35)
course.grid(row=3, column=0, padx=6, pady=0)

tk.Label(left_frame, text="Subject", bg="deepskyblue", fg="black", font=("Arial", 12, "bold")).grid(row=2, column=5, padx=0, pady=0, sticky="w")
subject_name = tk.Entry(left_frame, width=35)
subject_name.grid(row=3, column=5, padx=0, pady=0)


#third row

tk.Label(left_frame,text="Year",bg="deepskyblue",fg="black",font=("Arial",12,"bold")).grid(row=4,column=0,padx=5,pady=0,sticky="w")
year = tk.Entry(left_frame,width=35)
year.grid(row=5,column=0,padx=6,pady=0)


tk.Label(left_frame,text="Age",bg="deepskyblue",fg="black",font=("Arial",12,"bold")).grid(row=4,column=5,padx=0,pady=0,sticky="w")
age = tk.Entry(left_frame,width=35)
age.grid(row=5,column=5,padx=0,pady=0)



#fourth row
tk.Label(left_frame,text="Gender",bg="deepskyblue",fg="black",font=("Arial",12,"bold")).grid(row=6,column=0,padx=5,pady=0,sticky="w")
gender = tk.Entry(left_frame,width=35)
gender.grid(row=7,column=0,padx=6,pady=0)

tk.Label(left_frame,text="Date of Birth",bg="deepskyblue",fg="black",font=("Arial",12,"bold")).grid(row=6,column=5,padx=0,pady=0,sticky="w")
date_of_birth = tk.Entry(left_frame,width=35)
date_of_birth.grid(row=7,column=5,padx=0,pady=0)

#fifth row
tk.Label(left_frame,text="Mobile No",bg="deepskyblue",fg="black",font=("Arial",12,"bold")).grid(row=8,column=0,padx=5,pady=0,sticky="w")
mobile_no = tk.Entry(left_frame,width=35)
mobile_no.grid(row=9,column=0,padx=6,pady=0)

tk.Label(left_frame,text="Email ID",bg="deepskyblue",fg="black",font=("Arial",12,"bold")).grid(row=8,column=5,padx=0,pady=0,sticky="w")
email_id = tk.Entry(left_frame,width=35)
email_id.grid(row=9,column=5,padx=0,pady=0)

#sixth row
tk.Label(left_frame,text="Location",bg="deepskyblue",fg="black",font=("Arial",12,"bold")).grid(row=10,column=0,padx=5,pady=0,sticky="w")
location = tk.Entry(left_frame,width=35)
location.grid(row=11,column=0,padx=6,pady=0)

tk.Label(left_frame,text="Student_id",bg="deepskyblue",fg="black",font=("Arial",12,"bold")).grid(row=10,column=5,padx=0,pady=0,sticky="w")
student_id = tk.Entry(left_frame,width=35,state="disabled")
student_id.grid(row=11,column=5,padx=0,pady=0)

#create button in left frame
button=Button(left_frame,text="Submit",bg="lightgray",fg="black",command = submit_student,font=("Arial",13,"bold")).grid(row=12,column=2,pady=30,sticky="s")



#add buttons in Right frame

right_frame.grid_columnconfigure(0, weight=1)  # makes column expandable

Button(right_frame, text="Add New", font=("Arial",12,"bold"),command = add_new, width=10).grid(row=0, column=0, pady=(50,10))
Button(right_frame, text="View Details", font=("Arial",12,"bold"),command = view_students, width=10).grid(row=1, column=0, pady=10)
Button(right_frame, text="Update", font=("Arial",12,"bold"), command = update_student,width=10).grid(row=2, column=0, pady=10)
Button(right_frame, text="Delete", font=("Arial",12,"bold"),command = delete_student, width=10).grid(row=3, column=0, pady=10)
Button(right_frame, text="Clear", font=("Arial",12,"bold"),command = clear_form, width=10).grid(row=4, column=0, pady=10)
Button(right_frame, text="Exit", font=("Arial",12,"bold"), command = exit_app, width=10).grid(row=5, column=0, pady=10)





window.mainloop()
