import tkinter as tk
from tkinter import ttk,filedialog
import json
from school_management_classes import Person, Student, Instructor, Course , load_from_json, save_to_json
from tkinter import simpledialog
from tkinter import messagebox
from data_validation import validate_age,validate_course_id,validate_course_name,validate_email,validate_instructor_id,validate_name,validate_student_id
import csv
import sqlite3
import shutil
from database_schemas import db_add_student, db_add_instructor, db_add_course, db_update_student, db_update_instructor, db_update_course, delete_student, delete_instructor, delete_course, db_assign_course_to_instructor, db_register_student_to_course

#sample data for demonstration 
instructor_dict = {"Prof.Iman":Instructor("Prof.Iman", "25", "iman@hotmail.com", "1001", []),
    "Prof. Ali": Instructor("Prof. Ali", "38", "ali@gmail.com", "1002", []),
    "Prof. Ahmad": Instructor("Prof. Ahmad", "50", "ahmad@aub.com", "1003", [])
}

course_dict= {"EECE 435L": Course("EECE 435L", "Software Engineering Lab",None,[])}
student_dict={"Yasmeen":Student("Yasmeen",21,"ytl00@mail.aub.edu",202202478,[])}

# Main application window
root = tk.Tk()
root.title("School Management System")
root.configure(bg='light gray')  
root.geometry("1200x700")  

# Mian Grid Configuration 
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
for i in range(6):
    root.grid_columnconfigure(i, weight=1)


##  FUNCTIONS ###
def add_student():
    """
    Adds a student to the database and updates the GUI.

    This function retrieves student details (name, age, email, student ID) from input fields
    and the selected courses from the listbox. It then creates a Student object, stores the
    student in both an internal dictionary and the database, and refreshes the GUI components.

    The function also handles any errors that occur during student creation or database insertion.

    :raises Exception: If there is an error while creating the Student object or adding the student to the database.

    :return: None
    """
    name = name_entry.get()
    age = age_entry.get()
    email = email_entry.get()
    student_id = student_id_entry.get()
    selected_indices = courses_listbox.curselection()  # Get selected indices
    selected_courses = [course_dict[courses_listbox.get(i)] for i in selected_indices]
    print(f"Student Name: {name}, Age: {age}, Email: {email}, ID: {student_id}, Registered Courses: {selected_courses}")

    try:
        student= Student(name,age,email,student_id,selected_courses)
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return

    student_dict[name]= student
    try:
        db_add_student(student_id, name, age, email)
        messagebox.showinfo("Success", "Student added successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return
    # Clear all fields
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    student_id_entry.delete(0, tk.END)
    courses_listbox.selection_clear(0, tk.END)

    update_enrolled_students_listbox()
    setup_course_registration_ui()
    refresh_treeviews()


def add_instructor():
    """
    Adds an instructor to the database and updates the GUI.

    This function retrieves instructor details (name, age, email, instructor ID) from input fields,
    along with the selected courses from the listbox. It creates an Instructor object, stores the
    instructor in both an internal dictionary and the database, and refreshes the relevant GUI components.

    The function also handles errors that occur during instructor creation or database insertion.

    :raises Exception: If there is an error while creating the Instructor object or adding the instructor to the database.

    :return: None
    """
    name = instructor_name_entry.get()
    age = instructor_age_entry.get()
    email = instructor_email_entry.get()
    instructor_id = instructor_id_entry.get()
    selected_indices = instructor_courses_listbox.curselection()
    assigned_courses = [course_dict[instructor_courses_listbox.get(i)] for i in selected_indices]
    print(f"Instructor Name: {name}, Age: {age}, Email: {email}, ID: {instructor_id}, Assigned Courses: {assigned_courses}")
    
    try:
        instructor= Instructor(name,age,email,instructor_id,assigned_courses)
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return
    instructor_dict[name]=instructor
    try:
        db_add_instructor(instructor_id, name, age, email)
        messagebox.showinfo("Success", "Instructor added successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return
    instructor_name_entry.delete(0, tk.END)
    instructor_age_entry.delete(0, tk.END)
    instructor_email_entry.delete(0, tk.END)
    instructor_id_entry.delete(0, tk.END)
    instructor_courses_listbox.selection_clear(0, tk.END)

    update_instructor_combobox()
    setup_instructor_assignment_ui()
    refresh_treeviews()


def add_course():
    """
    Adds a course to the database and updates the GUI.

    This function retrieves course details (course ID, course name) from input fields,
    along with the selected instructor and enrolled students from the listboxes. It creates 
    a Course object, stores the course in both an internal dictionary and the database, 
    and refreshes the relevant GUI components.

    The function also handles any errors that occur during course creation or database insertion.

    :raises Exception: If there is an error while creating the Course object or adding the course to the database.

    :return: None
    """
    course_id = course_id_entry.get()
    course_name = course_name_entry.get()
    selected_instructor = instructor_dict[instructor_combobox.get()] if instructor_combobox.get() else None
    selected_indices = enrolled_students_listbox.curselection()
    enrolled_students = [student_dict[enrolled_students_listbox.get(i)] for i in selected_indices]
    print(f"Course ID: {course_id}, Name: {course_name}, Instructor: {selected_instructor}, Enrolled Students: {enrolled_students}")
    
    try:
        course= Course(course_id,course_name, selected_instructor, enrolled_students)
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return

    course_dict[course_id]=course
    try:
        db_add_course(course_id, course_name, selected_instructor)
        messagebox.showinfo("Success", "Course added successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return
    course_id_entry.delete(0, tk.END)
    course_name_entry.delete(0, tk.END)
    instructor_combobox.set('')
    enrolled_students_listbox.selection_clear(0, tk.END)

    update_courses_listbox()
    update_instructor_courses_listbox()
    setup_course_registration_ui()
    setup_instructor_assignment_ui()
    refresh_treeviews()
   

# Define colors for sections
section_color = '#f0f0f0'  # Light gray for section background
title_color = '#333333'  # Dark gray for titles


# Define frame styles
frame_style = {'padx': 5, 'pady': 5, 'sticky': 'nsew'}

# LabelFrames for different sections
frame_student = tk.LabelFrame(root, text="Student Details", bg=section_color, fg=title_color)
frame_instructor = tk.LabelFrame(root, text="Instructor Details", bg=section_color, fg=title_color)
frame_course = tk.LabelFrame(root, text="Course Details", bg=section_color, fg=title_color)
frame_course_registration = tk.LabelFrame(root, text="Course Registration", bg=section_color, fg=title_color)
frame_instructor_assignment = tk.LabelFrame(root, text="Instructor Assignment", bg=section_color, fg=title_color)

# Grid placement for frames
frame_student.grid(row=0, column=0, **frame_style)
frame_instructor.grid(row=0, column=1, **frame_style)
frame_course.grid(row=0, column=2, **frame_style)
frame_course_registration.grid(row=0, column=3, **frame_style)
frame_instructor_assignment.grid(row=0, column=4, columnspan=2, **frame_style)


### STUDENT SECTION ###
tk.Label(frame_student, text="Student Name:", bg=section_color).grid(row=0, column=0)
tk.Label(frame_student, text="Student Age:", bg=section_color).grid(row=1, column=0)
tk.Label(frame_student, text="Student Email:", bg=section_color).grid(row=2, column=0)
tk.Label(frame_student, text="Student ID:", bg=section_color).grid(row=3, column=0)
tk.Label(frame_student, text="Courses:", bg=section_color).grid(row=4, column=0)

name_entry = tk.Entry(frame_student)
age_entry = tk.Entry(frame_student)
email_entry = tk.Entry(frame_student)
student_id_entry = tk.Entry(frame_student)

name_entry.grid(row=0, column=1)
age_entry.grid(row=1, column=1)
email_entry.grid(row=2, column=1)
student_id_entry.grid(row=3, column=1)

courses_listbox = tk.Listbox(frame_student, selectmode='multiple', height=len(course_dict))
for course_id in course_dict:
    courses_listbox.insert(tk.END, course_id)
courses_listbox.grid(row=4, column=1)

tk.Button(frame_student, text="Add Student", command=add_student).grid(row=5, column=0, columnspan=2)

### INSTRUCTOR SECTION ###
tk.Label(frame_instructor, text="Instructor Name:", bg=section_color).grid(row=0, column=0)
tk.Label(frame_instructor, text="Instructor Age:", bg=section_color).grid(row=1, column=0)
tk.Label(frame_instructor, text="Instructor Email:", bg=section_color).grid(row=2, column=0)
tk.Label(frame_instructor, text="Instructor ID:", bg=section_color).grid(row=3, column=0)
tk.Label(frame_instructor, text="Assigned Courses:", bg=section_color).grid(row=4, column=0)

instructor_name_entry = tk.Entry(frame_instructor)
instructor_age_entry = tk.Entry(frame_instructor)
instructor_email_entry = tk.Entry(frame_instructor)
instructor_id_entry = tk.Entry(frame_instructor)

instructor_name_entry.grid(row=0, column=1)
instructor_age_entry.grid(row=1, column=1)
instructor_email_entry.grid(row=2, column=1)
instructor_id_entry.grid(row=3, column=1)

instructor_courses_listbox = tk.Listbox(frame_instructor, selectmode='multiple', height=len(course_dict))
for course_id in course_dict:
    instructor_courses_listbox.insert(tk.END, course_id)
instructor_courses_listbox.grid(row=4, column=1)

tk.Button(frame_instructor, text="Add Instructor", command=add_instructor).grid(row=5, column=0, columnspan=2)

### COURSE SECTION ###
tk.Label(frame_course, text="Course ID:", bg=section_color).grid(row=0, column=0)
tk.Label(frame_course, text="Course Name:", bg=section_color).grid(row=1, column=0)
tk.Label(frame_course, text="Instructor:", bg=section_color).grid(row=2, column=0)
tk.Label(frame_course, text="Enrolled Students:", bg=section_color).grid(row=3, column=0)

course_id_entry = tk.Entry(frame_course)
course_name_entry = tk.Entry(frame_course)
course_id_entry.grid(row=0, column=1)
course_name_entry.grid(row=1, column=1)

instructor_combobox = ttk.Combobox(frame_course, values=list(instructor_dict.keys()))
instructor_combobox.grid(row=2, column=1)

enrolled_students_listbox = tk.Listbox(frame_course, selectmode='multiple', height=len(student_dict))
for name in student_dict:
    enrolled_students_listbox.insert(tk.END, name)
enrolled_students_listbox.grid(row=3, column=1)

tk.Button(frame_course, text="Add Course", command=add_course).grid(row=4, column=0, columnspan=2)

def update_courses_listbox():
    """
    Updates the courses listbox in the GUI.

    This function clears the current content of the courses listbox, adjusts its height
    based on the number of courses in the `course_dict`, and repopulates the listbox with 
    the updated list of course IDs.

    :return: None
    """
    courses_listbox.delete(0, tk.END)
    courses_listbox.config(height=len(course_dict))
    for course_id in course_dict:
        courses_listbox.insert(tk.END, course_id)

def update_instructor_courses_listbox():
    """
    Updates the instructor courses listbox in the GUI.

    This function clears the current content of the instructor courses listbox, adjusts its height
    based on the number of courses in the `course_dict`, and repopulates the listbox with the 
    updated list of course IDs.

    :return: None
    """
    instructor_courses_listbox.delete(0, tk.END)
    instructor_courses_listbox.config(height=len(course_dict))
    for course_id in course_dict:
        instructor_courses_listbox.insert(tk.END, course_id)

def update_enrolled_students_listbox():
    """
    Updates the enrolled students listbox in the GUI.

    This function clears the current content of the enrolled students listbox, adjusts its height
    based on the number of students in `student_dict`, and repopulates the listbox with the 
    updated list of student names.

    :return: None
    """
    enrolled_students_listbox.delete(0, tk.END)
    enrolled_students_listbox.config(height=len(student_dict))
    for name in student_dict:
        enrolled_students_listbox.insert(tk.END, name)

def update_instructor_combobox():
    """
    Updates the instructor combobox in the GUI.

    This function retrieves the list of instructor names from `instructor_dict`
    and updates the combobox to reflect the current list of available instructors.

    :return: None
    """
    instructor_keys = list(instructor_dict.keys())
    instructor_combobox['values'] = instructor_keys


###  COURSE REGISTRATION FUNCTION AND UI  ###
def setup_course_registration_ui():
    """
    Sets up the UI for course registration in the GUI.

    This function creates and configures the widgets (labels, comboboxes, and a button)
    necessary for registering students to courses. It places the widgets on the grid 
    and populates the comboboxes with the available students and courses.

    The 'Register Course' button is connected to the `register_course()` function, which 
    handles the actual course registration logic.

    :return: None
    """
    # Comboboxes and Labels
    tk.Label(frame_course_registration, text="Select Student:", bg=section_color).grid(row=0, column=0, padx=10, pady=10)
    tk.Label(frame_course_registration, text="Select Course:", bg=section_color).grid(row=1, column=0, padx=10, pady=10)
    
    student_combobox = ttk.Combobox(frame_course_registration, width=20)
    course_combobox = ttk.Combobox(frame_course_registration, width=20)
    
    # Buttons
    register_button = tk.Button(frame_course_registration, text="Register Course", command=lambda: register_course(student_combobox.get(), course_combobox.get()))
    
    # Placement
    student_combobox.grid(row=0, column=1, padx=10, pady=10)
    course_combobox.grid(row=1, column=1, padx=10, pady=10)
    register_button.grid(row=2, column=0, columnspan=2)

    update_comboboxes(student_combobox, course_combobox)

def register_course(student_name, course_id):
    """
    Registers a student to a course and updates the database and GUI.

    This function retrieves the student and course based on the provided student name
    and course ID. If valid, the student is registered for the course, and the registration
    is added to the database. The function also updates the course with the enrolled student
    and refreshes the GUI.

    :param student_name: The name of the student to be registered (string).
    :param course_id: The ID of the course the student is registering for (string).
    :raises KeyError: If the student or course does not exist in the respective dictionaries.

    :return: None
    """
    student = student_dict.get(student_name)
    course = course_dict.get(course_id)
    if student and course:
        student.register_course(course)
        db_register_student_to_course(student_name,course_id)
        print(f"{student_name} has been registered to {course_id}")
    else:
        print("Invalid student or course selection")
    course.add_student(student)
    refresh_treeviews()

###  INSTRUCTOR ASSIGNMENT FUNCTION AND UI  ###
def setup_instructor_assignment_ui():
    """
    Sets up the UI for assigning courses to instructors in the GUI.

    This function creates and configures the widgets (labels, comboboxes, and a button) 
    necessary for assigning courses to instructors. It places the widgets on the grid 
    and populates the comboboxes with the list of available instructors and courses.

    The 'Assign Course' button is connected to the `assign_course_to_instructor()` function, 
    which handles the logic of assigning a course to an instructor.

    :return: None
    """
    # Comboboxes and Labels
    tk.Label(frame_instructor_assignment, text="Select Instructor:", bg=section_color).grid(row=0, column=0, padx=10, pady=10)
    tk.Label(frame_instructor_assignment, text="Select Course:", bg=section_color).grid(row=1, column=0, padx=10, pady=10)
    
    instructor_combobox = ttk.Combobox(frame_instructor_assignment, width=20)
    course_combobox = ttk.Combobox(frame_instructor_assignment, width=20)
    
    # Buttons
    assign_button = tk.Button(frame_instructor_assignment, text="Assign Course", command=lambda: assign_course_to_instructor(instructor_combobox.get(), course_combobox.get()))
    
    # Placement
    instructor_combobox.grid(row=0, column=1, padx=10, pady=10)
    course_combobox.grid(row=1, column=1, padx=10, pady=10)
    assign_button.grid(row=2, column=0, columnspan=2)

    update_instructor_course_comboboxes(instructor_combobox, course_combobox)

def assign_course_to_instructor(instructor_name, course_id):
    """
    Assigns a course to an instructor and updates the database and GUI.

    This function retrieves the instructor and course objects based on the provided 
    instructor name and course ID. If both are valid, it assigns the course to the 
    instructor, updates the database, and refreshes the GUI components to reflect 
    the new assignment.

    :param instructor_name: The name of the instructor to be assigned to a course (string).
    :param course_id: The ID of the course to assign to the instructor (string).
    :raises KeyError: If the instructor or course does not exist in the respective dictionaries.

    :return: None
    """
    instructor = instructor_dict.get(instructor_name)
    course = course_dict.get(course_id)
    if instructor and course:
        instructor.assign_course(course)
        db_assign_course_to_instructor(instructor_name, course_id)
        print(f"{instructor_name} has been assigned to {course_id}")
    else:
        print("Invalid instructor or course selection")
    course.instructor = instructor
    refresh_treeviews()

### Helper Functions ###
def update_comboboxes(student_combobox, course_combobox):
    """
    Updates the student and course comboboxes in the GUI.

    This function populates the student combobox with the list of available student names 
    from `student_dict`, and the course combobox with the list of available course IDs 
    from `course_dict`.

    :param student_combobox: The combobox for selecting students in the GUI.
    :param course_combobox: The combobox for selecting courses in the GUI.

    :return: None
    """
    student_combobox['values'] = list(student_dict.keys())
    course_combobox['values'] = list(course_dict.keys())

def update_instructor_course_comboboxes(instructor_combobox, course_combobox):
    """
    Updates the instructor and course comboboxes in the GUI.

    This function populates the instructor combobox with the list of available instructor names 
    from `instructor_dict`, and the course combobox with the list of available course IDs 
    from `course_dict`.

    :param instructor_combobox: The combobox for selecting instructors in the GUI.
    :param course_combobox: The combobox for selecting courses in the GUI.

    :return: None
    """
    instructor_combobox['values'] = list(instructor_dict.keys())
    course_combobox['values'] = list(course_dict.keys())


### Tree Setup ###
def setup_treeviews():
    """
    Sets up the Treeview widgets for displaying students, instructors, and courses in the GUI.

    This function creates labeled frames and Treeview widgets for displaying information
    about students, instructors, and courses. Each Treeview is populated with the corresponding
    data from `student_dict`, `instructor_dict`, and `course_dict`. Scrollbars are added to
    each Treeview for easier navigation.

    The Treeviews display columns such as name, age, email, student/instructor ID, courses, 
    and assigned/enrolled students.

    :return: None
    """
    global student_tree, instructor_tree, course_tree

    # Create labeled frames for each category to hold the Treeview and Scrollbars
    student_frame = ttk.LabelFrame(root, text="Students", padding=10)
    instructor_frame = ttk.LabelFrame(root, text="Instructors", padding=10)
    course_frame = ttk.LabelFrame(root, text="Courses", padding=10)
    student_frame.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=5, pady=5)
    instructor_frame.grid(row=1, column=2, columnspan=2, sticky='nsew', padx=5, pady=5)
    course_frame.grid(row=1, column=4, columnspan=2, sticky='nsew', padx=5, pady=5)

    # Setup for each Treeview
    student_tree = ttk.Treeview(student_frame, columns=("Name", "Age", "Email", "Student ID", "Courses"), show="headings", height=8)
    instructor_tree = ttk.Treeview(instructor_frame, columns=("Name", "Age", "Email", "Instructor ID", "Assigned Courses"), show="headings", height=8)
    course_tree = ttk.Treeview(course_frame, columns=("Course ID", "Course Name", "Instructor", "Enrolled Students"), show="headings", height=8)
    treeviews = [student_tree, instructor_tree, course_tree]

    for tree in treeviews:
        for col in tree["columns"]:
            tree.heading(col, text=col.replace("_", " "))
            tree.column(col, width=120, anchor="w")

    setup_scrollbars(student_frame, student_tree)
    setup_scrollbars(instructor_frame, instructor_tree)
    setup_scrollbars(course_frame, course_tree)

    for name in student_dict:
        populate_treeview(student_tree, student_dict[name])
        
    for name in instructor_dict:
        populate_treeview(instructor_tree, instructor_dict[name])

    for course_id in course_dict:
        populate_treeview(course_tree, course_dict[course_id])

def setup_scrollbars(frame, tree):
    """
    Sets up vertical and horizontal scrollbars for a Treeview widget in the GUI.

    This function adds both vertical and horizontal scrollbars to a Treeview widget. 
    The scrollbars are linked to the Treeview's scrolling functionality and are placed 
    inside the specified frame. The frame's grid configuration is adjusted to ensure 
    proper resizing behavior for the scrollbars and Treeview.

    :param frame: The frame that contains the Treeview and scrollbars.
    :param tree: The Treeview widget to which the scrollbars are being added.

    :return: None
    """
    # Scrollbars for Treeview
    v_scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    h_scroll = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
    tree.grid(row=0, column=0, sticky='nsew')
    v_scroll.grid(row=0, column=1, sticky='ns')
    h_scroll.grid(row=1, column=0, sticky='ew')
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)


def populate_treeview(tree, record):
    """
    Populates a Treeview widget with a student's, instructor's, or course's details.

    This function inserts data into a Treeview widget based on the type of `record` 
    provided. It handles three types of records:
    - Student: Inserts student name, age, email, student ID, and registered courses.
    - Instructor: Inserts instructor name, age, email, instructor ID, and assigned courses.
    - Course: Inserts course ID, course name, instructor name, and enrolled students.

    :param tree: The Treeview widget where the record will be displayed.
    :param record: The record object to be inserted (could be a Student, Instructor, or Course).

    :return: None
    """
    if isinstance(record, Student):
        courses = ', '.join([course.course_id for course in record.registered_courses]) # Join course names by comma
        tree.insert('', 'end', values=(record.name, record.age, record.get_email(), record.student_id, courses))
    
    elif isinstance(record, Instructor):
        assigned_courses = ', '.join([course.course_id for course in record.assigned_courses])
        tree.insert('', 'end', values=(record.name, record.age, record.get_email(), record.instructor_id, assigned_courses))
    
    elif isinstance(record, Course):
        instructor_name = record.instructor.name if record.instructor else "No instructor assigned"
        enrolled_students = ', '.join([student.name for student in record.enrolled_students])
        tree.insert('', 'end', values=(record.course_id, record.course_name, instructor_name, enrolled_students))

def refresh_treeviews():
    """
    Refreshes the Treeview widgets for students, instructors, and courses.

    This function clears all existing entries from the student, instructor, and course 
    Treeviews, and then repopulates them with the updated data from `student_dict`, 
    `instructor_dict`, and `course_dict`.

    :return: None
    """
    for tree in [student_tree, instructor_tree, course_tree]:
        tree.delete(*tree.get_children())  # Clear existing entries in the treeview
    
    for name in student_dict:
        populate_treeview(student_tree, student_dict[name])
    
    for name in instructor_dict:
        populate_treeview(instructor_tree, instructor_dict[name])

    for course_id in course_dict:
        populate_treeview(course_tree, course_dict[course_id])


def setup_search(): # Setup search areas
    """
    Sets up the search interface in the GUI.

    This function creates a search area with three search options: 
    - Search by Person ID
    - Search by Person Name
    - Search by Course ID

    Each search option has an entry field and a corresponding button that triggers 
    the `search_all()` function based on the input. Additionally, there is a 'Refresh Back' 
    button that refreshes the Treeviews to display all entries again.

    :return: None
    """
    frame_search = tk.Frame(root)
    frame_search.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky='ew')

    # Search by ID
    tk.Label(frame_search, text="Search by Person ID:").grid(row=0, column=0, padx=10)
    entry_id = tk.Entry(frame_search)
    entry_id.grid(row=0, column=1, padx=10)
    tk.Button(frame_search, text="Search", command=lambda: search_all('id', entry_id.get())).grid(row=0, column=2, padx=10)

    # Search by Name
    tk.Label(frame_search, text="Search by Person Name:").grid(row=1, column=0, padx=10)
    entry_name = tk.Entry(frame_search)
    entry_name.grid(row=1, column=1, padx=10)
    tk.Button(frame_search, text="Search", command=lambda: search_all('name', entry_name.get())).grid(row=1, column=2, padx=10)

    # Search by Course ID
    tk.Label(frame_search, text="Search by Course ID:").grid(row=2, column=0, padx=10)
    entry_course_id = tk.Entry(frame_search)
    entry_course_id.grid(row=2, column=1, padx=10)
    tk.Button(frame_search, text="Search", command=lambda: search_all('course_id', entry_course_id.get())).grid(row=2, column=2, padx=10)

    #Refresh Back
    # Search by Course ID
    tk.Button(frame_search, text="Refresh Back", command=refresh_treeviews).grid(row=3, column=2, padx=10)

def search_all(search_type, search_value):
    """
    Searches for records across students, instructors, and courses based on the provided search type and value.

    This function performs a case-insensitive search for a specific value across student, instructor, and course 
    records based on the selected search type (`id`, `name`, or `course_id`). The search value is stripped of 
    leading and trailing whitespace and converted to lowercase for comparison.

    The function applies the search filter to all relevant Treeviews:
    - If searching by `id`, it checks for matching student or instructor IDs.
    - If searching by `name`, it checks for matching student or instructor names.
    - If searching by `course_id`, it checks for matching course IDs.

    :param search_type: The type of search to perform (either 'id', 'name', or 'course_id').
    :param search_value: The value to search for in the records.
    
    :return: None
    """
    # Lowercase and strip the search value
    search_value = search_value.lower().strip()

    if search_type == 'id':
        filter_criteria = lambda record: search_value == str(record.student_id) if hasattr(record, 'student_id') else (search_value == str(record.instructor_id) if hasattr(record, 'instructor_id') else False)
    elif search_type == 'name':
        filter_criteria = lambda record: search_value in record.name.lower() if hasattr(record, 'name') else False
    elif search_type == 'course_id':
        filter_criteria = lambda record: search_value == record.course_id.lower() if hasattr(record, 'course_id') else False
    else:
        return

    # Apply the filter to the treeviews
    filter_treeview(student_tree, student_dict, filter_criteria)
    filter_treeview(instructor_tree, instructor_dict, filter_criteria)
    filter_treeview(course_tree, course_dict, filter_criteria)

def filter_treeview(tree, data_dict, filter_criteria):
    """
    Filters and displays records in a Treeview widget based on a specified filter criteria.

    This function clears the current entries in the given Treeview widget, iterates through 
    the records in `data_dict`, and populates the Treeview with records that meet the 
    provided `filter_criteria`.

    :param tree: The Treeview widget to update with filtered records.
    :param data_dict: The dictionary of records (students, instructors, or courses) to filter.
    :param filter_criteria: A lambda function used to determine whether a record should be displayed.
    
    :return: None
    """
    tree.delete(*tree.get_children())  # Clear existing entries
    for key, record in data_dict.items():
        if filter_criteria(record):
            populate_treeview(tree, record)


def setup_edit_delete_buttons(root):
    """
    Sets up the 'Edit' and 'Delete' buttons in the GUI for managing records.

    This function creates and places buttons in the main application window for editing 
    and deleting the selected item from the Treeview. The 'Edit Selected' button triggers 
    the `edit_record()` function, while the 'Delete Selected' button triggers the `delete_record()` function.

    :param root: The root window of the Tkinter application where the buttons will be placed.
    
    :return: None
    """
    # Buttons for editing and deleting the selected item in the student treeview
    edit_button = tk.Button(root, text="Edit Selected", command=edit_record)
    delete_button = tk.Button(root, text="Delete Selected", command=delete_record)

    edit_button.grid(row=2, column=4, padx=10, pady=10)
    delete_button.grid(row=2, column=5, padx=10, pady=10)



# Deleting a record
def delete_record():
    """
    Deletes the selected record from the Treeview and updates the corresponding data structure and database.

    This function identifies the currently selected item in the focused Treeview (students, instructors, or courses),
    confirms the deletion with the user, and then deletes the corresponding record from the internal data dictionary 
    and the SQLite database. If the deletion is successful, it removes the item from the Treeview and displays 
    a success message.

    The function supports deletion for:
    - Students: Removes from `student_dict` and the database via `delete_student()`.
    - Instructors: Removes from `instructor_dict` and the database via `delete_instructor()`.
    - Courses: Removes from `course_dict` and the database via `delete_course()`.

    :raises: Displays an error message if no item is selected or if the deletion is not confirmed.

    :return: None
    """
    focused_tree = root.focus_get()
    selected_item = focused_tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a record to delete")
        return

    if messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this record?"):
        item_values = focused_tree.item(selected_item, "values")
        if item_values[0] in student_dict:
            del student_dict[item_values[0]]
            delete_student(item_values[0])
        elif item_values[0] in instructor_dict:
            del instructor_dict[item_values[0]]
            delete_instructor(item_values[0])
        elif item_values[0] in course_dict:
            del course_dict[item_values[0]]
            delete_course(item_values[0])
        
        focused_tree.delete(selected_item)
        messagebox.showinfo("Deletion Successful", "Record deleted successfully")

def edit_record():
    """
    Opens an edit form for the selected student, instructor, or course.

    This function checks which record is currently selected in the respective Treeview 
    (students, instructors, or courses). Based on the selected record, it opens the appropriate 
    edit form, populating the form with the selected record's details.

    The function supports editing for:
    - Students: Calls `populate_edit_form_student()` to open the edit form for a student.
    - Instructors: Calls `populate_edit_form_instructor()` to open the edit form for an instructor.
    - Courses: Calls `populate_edit_form_course()` to open the edit form for a course.

    If no record is selected, it displays an error message prompting the user to select a record.

    :raises: Displays an error message if no record is selected.

    :return: None
    """
    # Determine which item is selected from the treeviews
    selected_student = student_tree.selection()
    selected_instructor = instructor_tree.selection()
    selected_course = course_tree.selection()

    if selected_student:
        item_values = student_tree.item(selected_student, "values")
        populate_edit_form_student(student_dict[item_values[0]])

    elif selected_instructor:
        item_values = instructor_tree.item(selected_instructor, "values")
        populate_edit_form_instructor(instructor_dict[item_values[0]])

    elif selected_course:
        item_values = course_tree.item(selected_course, "values")
        populate_edit_form_course(course_dict[item_values[0]])
    
    else:
        messagebox.showerror("Error", "Please select a record to delete")
        return

# Populate edit form for Student
def populate_edit_form_student(student):
    """
    Populates the edit form with the selected student's details for editing.

    This function clears any existing edit forms and opens a new form populated with 
    the details of the selected student. The form includes fields for the student's 
    name, age, email, and student ID. The user can modify these fields and save changes 
    using the 'Save Changes' button, which calls `update_student()` to apply the updates.

    :param student: The `Student` object whose details are to be edited.

    :return: None
    """
    clear_edit_forms()
    edit_frame = tk.LabelFrame(root, text="Edit Student", bg=section_color, fg=title_color)
    edit_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

    tk.Label(edit_frame, text="Name:", bg=section_color).grid(row=0, column=0)
    name_entry = tk.Entry(edit_frame)
    name_entry.insert(0, student.name)
    name_entry.grid(row=0, column=1)

    tk.Label(edit_frame, text="Age:", bg=section_color).grid(row=1, column=0)
    age_entry = tk.Entry(edit_frame)
    age_entry.insert(0, student.age)
    age_entry.grid(row=1, column=1)

    tk.Label(edit_frame, text="Email:", bg=section_color).grid(row=2, column=0)
    email_entry = tk.Entry(edit_frame)
    email_entry.insert(0, student.get_email())
    email_entry.grid(row=2, column=1)

    tk.Label(edit_frame, text="ID:", bg=section_color).grid(row=3, column=0)
    student_id_entry = tk.Entry(edit_frame)
    student_id_entry.insert(0, student.student_id)
    student_id_entry.grid(row=3, column=1)

    tk.Button(edit_frame, text="Save Changes", command=lambda: update_student(student, name_entry, age_entry, email_entry, student_id_entry)).grid(row=4, column=1)

# Populate edit form for Instructor
def populate_edit_form_instructor(instructor):
    """
    Populates the edit form with the selected instructor's details for editing.

    This function clears any existing edit forms and opens a new form populated with 
    the details of the selected instructor. The form includes fields for the instructor's 
    name, age, email, and instructor ID. The user can modify these fields and save changes 
    using the 'Save Changes' button, which calls `update_instructor()` to apply the updates.

    :param instructor: The `Instructor` object whose details are to be edited.

    :return: None
    """
    clear_edit_forms()
    edit_frame = tk.LabelFrame(root, text="Edit Instructor", bg=section_color, fg=title_color)
    edit_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

    tk.Label(edit_frame, text="Name:", bg=section_color).grid(row=0, column=0)
    name_entry = tk.Entry(edit_frame)
    name_entry.insert(0, instructor.name)
    name_entry.grid(row=0, column=1)

    tk.Label(edit_frame, text="Age:", bg=section_color).grid(row=1, column=0)
    age_entry = tk.Entry(edit_frame)
    age_entry.insert(0, instructor.age)
    age_entry.grid(row=1, column=1)

    tk.Label(edit_frame, text="Email:", bg=section_color).grid(row=2, column=0)
    email_entry = tk.Entry(edit_frame)
    email_entry.insert(0, instructor.get_email())
    email_entry.grid(row=2, column=1)

    tk.Label(edit_frame, text="ID:", bg=section_color).grid(row=3, column=0)
    instructor_id_entry = tk.Entry(edit_frame)
    instructor_id_entry.insert(0, instructor.instructor_id)
    instructor_id_entry.grid(row=3, column=1)

    tk.Button(edit_frame, text="Save Changes", command=lambda: update_instructor(instructor, name_entry, age_entry, email_entry, instructor_id_entry)).grid(row=4, column=1)

# Populate edit form for Course
def populate_edit_form_course(course):
    """
    Populates the edit form with the selected course's details for editing.

    This function clears any existing edit forms and opens a new form populated with 
    the details of the selected course. The form includes fields for the course ID 
    and course name. The user can modify these fields and save changes using the 
    'Save Changes' button, which calls `update_course()` to apply the updates.

    :param course: The `Course` object whose details are to be edited.

    :return: None
    """
    clear_edit_forms()
    edit_frame = tk.LabelFrame(root, text="Edit Course", bg=section_color, fg=title_color)
    edit_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

    tk.Label(edit_frame, text="Course ID:", bg=section_color).grid(row=0, column=0)
    course_id_entry = tk.Entry(edit_frame)
    course_id_entry.insert(0, course.course_id)
    course_id_entry.grid(row=0, column=1)

    tk.Label(edit_frame, text="Course Name:", bg=section_color).grid(row=1, column=0)
    course_name_entry = tk.Entry(edit_frame)
    course_name_entry.insert(0, course.course_name)
    course_name_entry.grid(row=1, column=1)

    tk.Button(edit_frame, text="Save Changes", command=lambda: update_course(course, course_id_entry, course_name_entry)).grid(row=4, column=1)

# Update student data
def update_student(student, name_entry, age_entry, email_entry, student_id_entry):
    """
    Updates the details of a student and refreshes the GUI.

    This function validates the input fields for the student's name, age, email, and student ID. 
    If the validation passes, it updates the corresponding `Student` object's attributes and 
    the SQLite database. The Treeview is refreshed to reflect the changes, and the edit form 
    is cleared.

    :param student: The `Student` object to be updated.
    :param name_entry: The entry widget containing the student's updated name.
    :param age_entry: The entry widget containing the student's updated age.
    :param email_entry: The entry widget containing the student's updated email.
    :param student_id_entry: The entry widget containing the student's updated ID.

    :raises Exception: If any of the validations for name, age, email, or student ID fail.

    :return: None
    """
    try:
        validate_name(name_entry.get())
        validate_age(int(age_entry.get()))
        validate_email(email_entry.get())
        validate_student_id(student_id_entry.get())
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return
    
    student.name = name_entry.get()
    student.age = age_entry.get()
    student._email = email_entry.get()
    student.student_id = student_id_entry.get()
    db_update_student(student_id_entry, name_entry, age_entry, email_entry)
    refresh_treeviews()
    clear_edit_forms()

# Update instructor data
def update_instructor(instructor, name_entry, age_entry, email_entry, instructor_id_entry):
    """
    Updates the details of an instructor and refreshes the GUI.

    This function validates the input fields for the instructor's name, age, email, and instructor ID.
    If the validation passes, it updates the corresponding `Instructor` object's attributes and 
    the SQLite database. The Treeview is refreshed to reflect the changes, and the edit form is cleared.

    :param instructor: The `Instructor` object to be updated.
    :param name_entry: The entry widget containing the instructor's updated name.
    :param age_entry: The entry widget containing the instructor's updated age.
    :param email_entry: The entry widget containing the instructor's updated email.
    :param instructor_id_entry: The entry widget containing the instructor's updated ID.

    :raises Exception: If any of the validations for name, age, email, or instructor ID fail.

    :return: None
    """
    try:
        validate_name(name_entry.get())
        validate_age(int(age_entry.get()))
        validate_email(email_entry.get())
        validate_instructor_id(instructor_id_entry.get())
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return
    
    instructor.name = name_entry.get()
    instructor.age = age_entry.get()
    instructor._email = email_entry.get()
    instructor.instructor_id = instructor_id_entry.get()
    db_update_instructor(instructor_id_entry, name_entry, age_entry, email_entry)
    refresh_treeviews()
    clear_edit_forms()

# Update course data
def update_course(course, course_id_entry, course_name_entry):
    """
    Updates the details of a course and refreshes the GUI.

    This function validates the input fields for the course ID and course name. 
    If the validation passes, it updates the corresponding `Course` object's attributes 
    and the SQLite database. The Treeview is refreshed to reflect the changes, and the 
    edit form is cleared.

    :param course: The `Course` object to be updated.
    :param course_id_entry: The entry widget containing the updated course ID.
    :param course_name_entry: The entry widget containing the updated course name.

    :raises Exception: If any of the validations for course ID or course name fail.

    :return: None
    """
    try:
        validate_course_id(course_id_entry.get())
        validate_course_name(course_name_entry.get())
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return
    
    course.course_id = course_id_entry.get()
    course.course_name = course_name_entry.get()
    db_update_course(course_id_entry, course_name_entry)
    refresh_treeviews()
    clear_edit_forms()

# Clear the edit forms before showing a new one
def clear_edit_forms():
    """
    Clears any existing edit forms from the GUI before displaying a new form.

    This function removes all widgets from row 2 of the main grid layout, which is where 
    the edit forms are displayed. After clearing the forms, it resets the search and 
    edit/delete buttons by calling `setup_search()` and `setup_edit_delete_buttons()`.

    :return: None
    """
    for widget in root.grid_slaves(row=2):
        widget.destroy()
    setup_search()
    setup_edit_delete_buttons(root)

def setup_save_data():
    """
    Sets up the buttons for saving, loading, exporting, and backing up data in the GUI.

    This function creates and places buttons in the main window for the following actions:
    - 'Save Data': Triggers the `save_data()` function to save current data.
    - 'Load Data': Triggers the `load_data()` function to load saved data.
    - 'Export to CSV': Triggers the `export_to_csv()` function to export data to a CSV file.
    - 'Backup Database': Triggers the `backup_database()` function to create a backup of the database.

    The buttons are placed in row 3 of the main grid layout.

    :return: None
    """
    save_button = tk.Button(root, text="Save Data", command=save_data)
    load_button = tk.Button(root, text="Load Data", command=load_data)
    csv_button = tk.Button(root, text="Export to CSV", command=export_to_csv)
    save_button.grid(row=3, column=0, padx=10, pady=10)
    load_button.grid(row=3, column=1, padx=10, pady=10)
    csv_button.grid(row=3, column=2, padx=10, pady=10)
    # Adding the Backup Button to the UI
    backup_button = tk.Button(root, text="Backup Database", command=backup_database)
    backup_button.grid(row=3, column=3, padx=10, pady=10)


def save_data():
    """
    Saves the current data (students, instructors, and courses) to a JSON file.

    This function converts the data from the internal dictionaries (`student_dict`, `instructor_dict`, `course_dict`) 
    into a serializable format by calling each object's `change_to_dictionary()` method. It then prompts the user 
    to select a file location and saves the data as a JSON file. If the process is successful, a success message 
    is shown; otherwise, an error message is displayed.

    :raises Exception: If the process of saving the data to a JSON file fails.

    :return: None
    """
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
    if not file_path:
        return

    try:
        # Convert data into serializable form using change_to_dictionary
        data = {
            "students": {name: student.change_to_dictionary() for name, student in student_dict.items()},
            "instructors": {name: instructor.change_to_dictionary() for name, instructor in instructor_dict.items()},
            "courses": {
                course_id: {
                    'course_id': course.course_id,
                    'course_name': course.course_name,
                    'instructor': course.instructor.change_to_dictionary() if course.instructor else None,  # Check if instructor exists
                    'enrolled_students': [student.change_to_dictionary() for student in course.enrolled_students] if course.enrolled_students else []
                }
                for course_id, course in course_dict.items()
            }
        }

        # Save to JSON file
        save_to_json(data, file_path)
        messagebox.showinfo("Success", "Data saved successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save data: {e}")


def load_data():
    """
    Loads data (students, instructors, and courses) from a JSON file into the application.

    This function prompts the user to select a JSON file containing saved data. It clears 
    the current data in `student_dict`, `instructor_dict`, and `course_dict`, and reconstructs 
    `Student`, `Instructor`, and `Course` objects from the loaded data. The data is then 
    displayed in the Treeview widgets, and a success message is shown upon successful loading.

    :raises Exception: If loading the JSON file or reconstructing the data fails, an error message is displayed.

    :return: None
    """
    file_path = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
    if not file_path:
        return

    try:
        # Load JSON data
        data = load_from_json(file_path)

        # Clear current data
        student_dict.clear()
        instructor_dict.clear()
        course_dict.clear()

        # Reconstruct objects from loaded data
        for name, student_data in data.get("students", {}).items():
            student = Student(
                student_data['name'], 
                student_data['age'], 
                student_data['email'], 
                student_data['student_id'], 
                []  # We'll populate courses later
            )
            student_dict[name] = student

        for name, instructor_data in data.get("instructors", {}).items():
            instructor = Instructor(
                instructor_data['name'], 
                instructor_data['age'], 
                instructor_data['email'], 
                instructor_data['instructor_id'], 
                []  # We'll populate assigned courses later
            )
            instructor_dict[name] = instructor

        for course_id, course_data in data.get("courses", {}).items():
            instructor = instructor_dict.get(course_data['instructor']['instructor_id']) if course_data['instructor'] else None
            enrolled_students = [student_dict[s['student_id']] for s in course_data['enrolled_students'] if s['student_id'] in student_dict]
            course = Course(
                course_data['course_id'], 
                course_data['course_name'], 
                instructor, 
                enrolled_students
            )
            course_dict[course_id] = course

        refresh_treeviews()
        messagebox.showinfo("Success", "Data loaded successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load data: {e}")

def export_to_csv():
    """
    Exports the current data (students, instructors, and courses) to a CSV file.

    This function prompts the user to select a location to save the CSV file. It exports the 
    details of students, instructors, and courses from `student_dict`, `instructor_dict`, and 
    `course_dict` into the CSV file with appropriate headers. Each student's registered courses, 
    instructor's assigned courses, and the course's enrolled students are included.

    A success message is displayed when the export completes successfully. If an error occurs 
    during the export, an error message is displayed.

    :raises Exception: If the export process fails due to file handling or data writing issues.

    :return: None
    """
    # Ask the user where to save the file
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])

    if not file_path:
        return  # If the user cancels the save dialog, do nothing
    
    try:
        # Open the file for writing
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)

            # Write header row for students
            writer.writerow(['Student Name', 'Age', 'Email', 'Student ID', 'Registered Courses'])
            for student in student_dict.values():
                courses = ', '.join([course.course_id for course in student.registered_courses])
                writer.writerow([student.name, student.age, student.get_email(), student.student_id, courses])

            # Write header row for instructors
            writer.writerow(['Instructor Name', 'Age', 'Email', 'Instructor ID', 'Assigned Courses'])
            for instructor in instructor_dict.values():
                assigned_courses = ', '.join([course.course_id for course in instructor.assigned_courses])
                writer.writerow([instructor.name, instructor.age, instructor.get_email(), instructor.instructor_id, assigned_courses])

            # Write header row for courses
            writer.writerow(['Course ID', 'Course Name', 'Instructor', 'Enrolled Students'])
            for course in course_dict.values():
                instructor_name = course.instructor.name if course.instructor else "No instructor"
                enrolled_students = ', '.join([student.name for student in course.enrolled_students])
                writer.writerow([course.course_id, course.course_name, instructor_name, enrolled_students])

        messagebox.showinfo("Success", "Records successfully exported to CSV")
    
    except Exception as e:
        messagebox.showerror("Error", f"Failed to export records to CSV: {e}")

def backup_database():
    """
    Creates a backup of the SQLite database and saves it to a user-specified location.

    This function prompts the user to choose a location and filename for saving the database backup.
    It then copies the existing SQLite database file (`school_management.db`) to the specified location. 
    A success message is shown upon successful backup creation. If an error occurs during the process, 
    an error message is displayed.

    :raises Exception: If the process of copying the database file fails.

    :return: None
    """
    # Ask the user where to save the backup file
    file_path = filedialog.asksaveasfilename(defaultextension=".db", filetypes=[("Database Files", "*.db")])

    if file_path:
        try:
            # Copy the database file to the user-specified location
            shutil.copyfile('school_management.db', file_path)
            messagebox.showinfo("Success", "Database backup created successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create database backup: {e}")

#UI Setup
setup_course_registration_ui()
setup_instructor_assignment_ui()
setup_edit_delete_buttons(root)
setup_treeviews()
setup_search()
setup_save_data()

# Start the Tkinter event loop
root.mainloop()
